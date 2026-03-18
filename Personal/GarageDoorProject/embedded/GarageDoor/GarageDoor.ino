// Required libraries (install via Arduino Library Manager):
//   ArduinoWebsockets  - Gil Maimon  (search "ArduinoWebsockets")
//   ArduinoJson        - Benoit Blanchon
//   ESP32Ping          - marian-craciunescu

#include <ArduinoJson.h>
#include <ArduinoWebsockets.h>
#include <ESPping.h>
#include <Preferences.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>

using namespace websockets;

// --- Motor pins --------------------------------------------------------------
const int MOTOR_PIN1 = 27;
const int MOTOR_PIN2 = 26;
const int ENABLE_PIN = 14;

const int PWM_FREQ       = 30000;
const int PWM_CHANNEL    = 0;
const int PWM_RESOLUTION = 8;
const int DUTY_CYCLE     = 200;

#define FORWARD  1
#define BACKWARD 0

// --- WiFi AP (setup mode) ----------------------------------------------------
const char *AP_SSID     = "GarageDoor-Setup";
const char *AP_PASSWORD = "setup1234";  // min 8 chars for WPA2
const int   WIFI_TIMEOUT_MS = 15000;

// --- Globals -----------------------------------------------------------------
struct Config {
  String wifiSSID;
  String wifiPass;
  String wsHost;   // backend hostname or IP, e.g. garagedoor.amai.bg or 192.168.1.50
  int    wsPort;   // 443 for wss (production), 8000 for ws (local)
  String wsToken;  // shared secret matching ESP_WS_TOKEN in backend .env
};

Preferences      prefs;
WebServer        server(80);
WebsocketsClient wsClient;

Config currentConfig;
bool   motorBusy      = false;
bool   configReceived = false;
Config pendingConfig;

// Persisted across reboots. Values: "open", "closed", "unknown".
String doorState = "unknown";

// --- Door state persistence --------------------------------------------------
String loadDoorState() {
  prefs.begin("garage", true);
  String s = prefs.getString("door", "closed");
  prefs.end();
  if (s == "unknown") s = "closed";
  return s;
}

void saveDoorState(const String &s) {
  prefs.begin("garage", false);
  prefs.putString("door", s);
  prefs.end();
}

// --- State reporting ---------------------------------------------------------
// Sends both door and motor state to the backend in a single message.
void sendState() {
  if (wsClient.available()) {
    String msg = "{\"door\":\"";
    msg += doorState;
    msg += "\",\"motor\":\"";
    msg += motorBusy ? "moving" : "idle";
    msg += "\"}";
    wsClient.send(msg);
    Serial.printf("State sent: door=%s motor=%s\n",
                  doorState.c_str(), motorBusy ? "moving" : "idle");
  }
}

// --- Motor control -----------------------------------------------------------
void stopMotor(const String &newDoorState) {
  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  ledcWrite(ENABLE_PIN, 0);
  motorBusy = false;
  Serial.println("Motor stopped");

  // Update and persist the new door position.
  doorState = newDoorState;
  saveDoorState(doorState);
  sendState();
}

// Triggers the motor. Direction and resulting door state are derived from
// the current doorState. If unknown, we default to FORWARD.
void triggerMotor() {
  if (motorBusy) {
    Serial.println("Motor busy - ignoring command");
    return;
  }

  // Pick direction and the state the door will be in after this run.
  int    direction    = FORWARD;
  String nextDoorState = "unknown";

  if (doorState == "closed") {
    direction     = FORWARD;   // open the door
    nextDoorState = "open";
  } else if (doorState == "open") {
    direction     = BACKWARD;  // close the door
    nextDoorState = "closed";
  } else {
    // Unknown - default to FORWARD, door state stays unknown.
    direction     = FORWARD;
    nextDoorState = "unknown";
  }

  motorBusy = true;
  sendState();  // broadcast motor=moving before blocking

  Serial.printf("Rotating %s (door: %s -> %s)\n",
                direction == FORWARD ? "FORWARD" : "BACKWARD",
                doorState.c_str(), nextDoorState.c_str());

  if (direction == FORWARD) {
    digitalWrite(MOTOR_PIN1, LOW);
    digitalWrite(MOTOR_PIN2, HIGH);
  } else {
    digitalWrite(MOTOR_PIN1, HIGH);
    digitalWrite(MOTOR_PIN2, LOW);
  }
  ledcWrite(ENABLE_PIN, DUTY_CYCLE);
  delay(2000);
  stopMotor(nextDoorState);
}

// --- Flash (NVS) config helpers ----------------------------------------------
Config loadConfig() {
  prefs.begin("garage", true);  // read-only
  Config c;
  c.wifiSSID = prefs.getString("ssid",     "");
  c.wifiPass = prefs.getString("wifiPass", "");
  c.wsHost   = prefs.getString("wsHost",   "");
  c.wsPort   = prefs.getInt   ("wsPort",   443);
  c.wsToken  = prefs.getString("wsToken",  "");
  prefs.end();
  return c;
}

void saveConfig(const Config &c) {
  prefs.begin("garage", false);  // read-write
  prefs.putString("ssid",     c.wifiSSID);
  prefs.putString("wifiPass", c.wifiPass);
  prefs.putString("wsHost",   c.wsHost);
  prefs.putInt   ("wsPort",   c.wsPort);
  prefs.putString("wsToken",  c.wsToken);
  prefs.end();
}

// --- WiFi connection ---------------------------------------------------------
bool connectWiFi(const Config &c) {
  if (c.wifiSSID.isEmpty()) {
    Serial.println("No WiFi credentials stored");
    return false;
  }

  Serial.printf("Connecting to WiFi: %s\n", c.wifiSSID.c_str());
  WiFi.mode(WIFI_STA);
  WiFi.begin(c.wifiSSID.c_str(), c.wifiPass.c_str());

  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - start > WIFI_TIMEOUT_MS) {
      Serial.println("\nWiFi timed out");
      WiFi.disconnect(true);
      return false;
    }
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nConnected. IP: %s\n", WiFi.localIP().toString().c_str());
  return true;
}

// --- Setup-mode captive portal -----------------------------------------------
static const char SETUP_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Garage Door Setup</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f0f2f5;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0;
      padding: 16px;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      padding: 2rem 1.75rem;
      width: 100%;
      max-width: 420px;
    }
    .logo {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 0.25rem;
    }
    h2 {
      text-align: center;
      margin: 0 0 0.25rem;
      color: #1a1a1a;
      font-size: 1.3rem;
    }
    .subtitle {
      text-align: center;
      font-size: 0.8rem;
      color: #999;
      margin-bottom: 1.5rem;
    }
    .section {
      background: #f8f9fb;
      border-radius: 8px;
      padding: 1rem 1rem 0.15rem;
      margin-bottom: 1rem;
    }
    .section-title {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #4f7df0;
      margin-bottom: 0.75rem;
    }
    label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      color: #444;
      margin-bottom: 0.2rem;
    }
    input {
      width: 100%;
      padding: 0.6rem 0.85rem;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 0.95rem;
      outline: none;
      background: #fff;
      transition: border-color 0.2s, box-shadow 0.2s;
      margin-bottom: 0.85rem;
    }
    input:focus {
      border-color: #4f7df0;
      box-shadow: 0 0 0 3px rgba(79,125,240,0.15);
    }
    .hint {
      font-size: 0.73rem;
      color: #aaa;
      margin-top: -0.65rem;
      margin-bottom: 0.85rem;
      line-height: 1.4;
    }
    button {
      width: 100%;
      padding: 0.8rem;
      background: #4f7df0;
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
    }
    button:hover  { background: #3a68da; }
    button:active { transform: scale(0.98); }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">&#127968;</div>
    <h2>Garage Door Setup</h2>
    <p class="subtitle">Configure WiFi and backend connection</p>

    <form method="POST" action="/save">
      <div class="section">
        <p class="section-title">WiFi Network</p>
        <label>Network name (SSID)</label>
        <input name="ssid" required placeholder="Your WiFi network">
        <label>Password</label>
        <input name="wifiPass" type="password" placeholder="Leave blank for open network">
      </div>

      <div class="section">
        <p class="section-title">Backend</p>
        <label>Hostname / IP</label>
        <input name="wsHost" required placeholder="garagedoor.amai.bg or 192.168.1.50">
        <p class="hint">Domain name or local IP - no https:// prefix</p>
        <label>Port</label>
        <input name="wsPort" type="number" value="443" min="1" max="65535">
        <p class="hint">443 for production (wss), 8000 for local network (ws)</p>
        <label>Device token</label>
        <input name="wsToken" type="password" required placeholder="Shared secret">
        <p class="hint">Must match ESP_WS_TOKEN in the backend .env file</p>
      </div>

      <button type="submit">Save &amp; Connect</button>
    </form>
  </div>
</body>
</html>
)rawliteral";

static const char SAVED_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Saved</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f0f2f5;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0;
      padding: 16px;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      padding: 2.5rem 2rem;
      text-align: center;
      max-width: 360px;
      width: 100%;
    }
    .icon { font-size: 3rem; margin-bottom: 0.75rem; }
    h2 { color: #27ae60; margin-bottom: 0.75rem; font-size: 1.3rem; }
    p { color: #666; line-height: 1.6; font-size: 0.9rem; }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">&#10003;</div>
    <h2>Credentials saved!</h2>
    <p>The device is now connecting to your WiFi and backend server.<br><br>
       This setup access point will disappear shortly.</p>
  </div>
</body>
</html>
)rawliteral";

void handleRoot() { server.send_P(200, "text/html", SETUP_HTML); }

void handleSave() {
  pendingConfig.wifiSSID = server.arg("ssid");
  pendingConfig.wifiPass = server.arg("wifiPass");
  pendingConfig.wsHost   = server.arg("wsHost");
  pendingConfig.wsPort   = server.arg("wsPort").toInt();
  if (pendingConfig.wsPort <= 0) pendingConfig.wsPort = 443;
  pendingConfig.wsToken  = server.arg("wsToken");

  saveConfig(pendingConfig);
  server.send_P(200, "text/html", SAVED_HTML);
  configReceived = true;
}

// Blocks until the user submits the setup form, then returns.
void runSetupMode() {
  Serial.printf("Entering setup mode. Connect to AP \"%s\" (pw: %s)\n",
                AP_SSID, AP_PASSWORD);

  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASSWORD);
  Serial.printf("Portal IP: %s\n", WiFi.softAPIP().toString().c_str());

  server.on("/",     HTTP_GET,  handleRoot);
  server.on("/save", HTTP_POST, handleSave);
  server.begin();

  configReceived = false;
  while (!configReceived) {
    server.handleClient();
    delay(10);
  }

  server.stop();
  WiFi.softAPdisconnect(true);
  delay(500);
}

// --- Internet connectivity check ---------------------------------------------
bool hasInternet() {
  Serial.println("Pinging 8.8.8.8...");
  if (Ping.ping(IPAddress(8, 8, 8, 8), 3)) return true;
  Serial.println("Pinging 1.1.1.1...");
  if (Ping.ping(IPAddress(1, 1, 1, 1), 3)) return true;
  return false;
}

// --- WebSocket ---------------------------------------------------------------
void onWsMessage(WebsocketsMessage msg) {
  Serial.printf("WS recv: %s\n", msg.data().c_str());

  StaticJsonDocument<128> doc;
  if (deserializeJson(doc, msg.data()) != DeserializationError::Ok) {
    Serial.println("JSON parse error - ignoring");
    return;
  }

  const char *action = doc["action"];
  if (action && strcmp(action, "trigger") == 0) {
    triggerMotor();
  }
}

void onWsEvent(WebsocketsEvent event, String data) {
  if (event == WebsocketsEvent::ConnectionOpened) {
    Serial.println("WebSocket connected");
    // Report current state so the backend syncs immediately on (re)connect.
    sendState();
  } else if (event == WebsocketsEvent::ConnectionClosed) {
    Serial.println("WebSocket disconnected");
  } else if (event == WebsocketsEvent::GotPing) {
    wsClient.pong();
  }
}

bool connectWS() {
  if (currentConfig.wsHost.isEmpty() || currentConfig.wsToken.isEmpty()) {
    Serial.println("No WebSocket config - skipping");
    return false;
  }

  wsClient.onMessage(onWsMessage);
  wsClient.onEvent(onWsEvent);

  bool useTls = (currentConfig.wsPort == 443);
  if (useTls) {
    // Skip CA verification - acceptable for a home device without a trust store.
    // The shared token still ensures only this device connects.
    wsClient.setInsecure();
  }

  String scheme = useTls ? "wss" : "ws";
  String url = scheme + "://" + currentConfig.wsHost + ":" +
               String(currentConfig.wsPort) + "/ws/esp?token=" + currentConfig.wsToken;
  Serial.printf("Connecting to %s\n", url.c_str());

  bool ok = wsClient.connect(url);
  if (!ok) {
    Serial.println("WebSocket connection failed");
  }
  return ok;
}

// --- setup / loop ------------------------------------------------------------
void setup() {
  Serial.begin(115200);

  // Motor init
  pinMode(MOTOR_PIN1, OUTPUT);
  pinMode(MOTOR_PIN2, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  ledcAttachChannel(ENABLE_PIN, PWM_FREQ, PWM_RESOLUTION, PWM_CHANNEL);

  // Stop motor and load persisted door state before anything else.
  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  ledcWrite(ENABLE_PIN, 0);
  doorState = loadDoorState();
  Serial.printf("Loaded door state: %s\n", doorState.c_str());

  // WiFi init: try stored credentials; on failure run setup portal and retry
  while (true) {
    currentConfig = loadConfig();
    if (connectWiFi(currentConfig)) break;
    runSetupMode();
  }

  if (hasInternet()) {
    Serial.println("Internet: OK");
    connectWS();
  } else {
    Serial.println("Internet: unreachable - WebSocket skipped");
  }
}

// Exponential backoff state for WebSocket reconnection
unsigned long wsNextRetryMs  = 0;
unsigned long wsRetryDelayMs = 2000;          // starts at 2 s
const unsigned long WS_RETRY_MAX_MS = 60000;  // caps at 60 s

void loop() {
  if (!currentConfig.wsHost.isEmpty() && !wsClient.available()) {
    unsigned long now = millis();
    if (now >= wsNextRetryMs) {
      Serial.printf("WebSocket disconnected - retrying in %lu s...\n",
                    wsRetryDelayMs / 1000);
      if (connectWS()) {
        wsRetryDelayMs = 2000;  // reset on success
      } else {
        wsRetryDelayMs = min(wsRetryDelayMs * 2, WS_RETRY_MAX_MS);
      }
      wsNextRetryMs = millis() + wsRetryDelayMs;
    }
  }
  wsClient.poll();
}
