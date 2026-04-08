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

const int PWM_FREQ = 30000;
const int PWM_CHANNEL = 0;
const int PWM_RESOLUTION = 8;
const int DUTY_CYCLE = 200;

#define FORWARD 1
#define BACKWARD 0

// --- WiFi AP (setup mode) ----------------------------------------------------
const char *AP_SSID = "GarageDoor-Setup";
const char *AP_PASSWORD = "setup1234"; // min 8 chars for WPA2
const int WIFI_TIMEOUT_MS = 15000;

// --- Reset button ------------------------------------------------------------
// Wire a push button between this pin and GND.
// Hold it down while powering on (or pressing RST) to clear all stored data.
const int RESET_BTN_PIN = 0; // GPIO0 is the BOOT button on most ESP32 devkits
const int RESET_HOLD_MS = 3000; // hold for 3 s to confirm

// --- Globals -----------------------------------------------------------------
struct Config {
  String wifiSSID;
  String wifiPass;
  // Full WebSocket base URL, e.g. wss://garage.amai.bg or
  // ws://192.168.1.50:8000
  String wsUrl;
  String wsToken; // shared secret matching ESP_WS_TOKEN in backend .env
};

Preferences prefs;
WebServer server(80);
WebsocketsClient wsClient;

Config currentConfig;
bool motorBusy = false;
bool configReceived = false;
Config pendingConfig;

// Persisted across reboots. Values: "open", "closed", "unknown".
String doorState = "unknown";

// --- Factory reset -----------------------------------------------------------
void checkFactoryReset() {
  pinMode(RESET_BTN_PIN, INPUT_PULLUP);

  if (digitalRead(RESET_BTN_PIN) != LOW)
    return;

  Serial.println("Reset button held - hold for 3 s to clear all data...");

  unsigned long start = millis();
  while (digitalRead(RESET_BTN_PIN) == LOW) {
    if (millis() - start >= RESET_HOLD_MS) {
      Serial.println("Clearing NVS...");
      prefs.begin("garage", false);
      prefs.clear();
      prefs.end();
      Serial.println("Restarting...");
      delay(500);
      ESP.restart();
    }
    delay(50);
  }
  Serial.println("Reset cancelled (released too early)");
}

// --- Door state persistence --------------------------------------------------
String loadDoorState() {
  prefs.begin("garage", true);
  String s = prefs.getString("door", "closed");
  prefs.end();
  if (s == "unknown")
    s = "closed";
  return s;
}

void saveDoorState(const String &s) {
  prefs.begin("garage", false);
  prefs.putString("door", s);
  prefs.end();
}

// --- State reporting ---------------------------------------------------------
void sendState() {
  if (wsClient.available()) {
    String msg = "{\"door\":\"";
    msg += doorState;
    msg += "\",\"motor\":\"";
    msg += motorBusy ? "moving" : "idle";
    msg += "\"}";
    wsClient.send(msg);
    Serial.printf("State sent: door=%s motor=%s\n", doorState.c_str(),
                  motorBusy ? "moving" : "idle");
  }
}

// --- Motor control -----------------------------------------------------------
void stopMotor(const String &newDoorState) {
  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  ledcWrite(ENABLE_PIN, 0);
  motorBusy = false;
  Serial.println("Motor stopped");

  doorState = newDoorState;
  saveDoorState(doorState);
  sendState();
}

void triggerMotor() {
  if (motorBusy) {
    Serial.println("Motor busy - ignoring command");
    return;
  }

  int direction = FORWARD;
  String nextDoorState = "unknown";

  if (doorState == "closed") {
    direction = FORWARD;
    nextDoorState = "open";
  } else if (doorState == "open") {
    direction = BACKWARD;
    nextDoorState = "closed";
  } else {
    direction = FORWARD;
    nextDoorState = "unknown";
  }

  motorBusy = true;
  sendState();

  Serial.printf("Motor: %s -> %s\n", doorState.c_str(), nextDoorState.c_str());

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
  prefs.begin("garage", true);
  Config c;
  c.wifiSSID = prefs.getString("ssid", "");
  c.wifiPass = prefs.getString("wifiPass", "");
  c.wsUrl = prefs.getString("wsUrl", "");
  c.wsToken = prefs.getString("wsToken", "");
  prefs.end();
  return c;
}

void saveConfig(const Config &c) {
  prefs.begin("garage", false);
  prefs.putString("ssid", c.wifiSSID);
  prefs.putString("wifiPass", c.wifiPass);
  prefs.putString("wsUrl", c.wsUrl);
  prefs.putString("wsToken", c.wsToken);
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
    .logo { text-align: center; font-size: 2.5rem; margin-bottom: 0.25rem; }
    h2 { text-align: center; margin: 0 0 0.25rem; color: #1a1a1a; font-size: 1.3rem; }
    .subtitle { text-align: center; font-size: 0.8rem; color: #999; margin-bottom: 1.5rem; }
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
    label { display: block; font-size: 0.82rem; font-weight: 600; color: #444; margin-bottom: 0.2rem; }
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
    input:focus { border-color: #4f7df0; box-shadow: 0 0 0 3px rgba(79,125,240,0.15); }
    .hint { font-size: 0.73rem; color: #aaa; margin-top: -0.65rem; margin-bottom: 0.85rem; line-height: 1.4; }
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
        <label>Backend URL</label>
        <input name="wsUrl" required placeholder="wss://garage.amai.bg">
        <p class="hint">Use wss:// for a secure connection (production) or ws:// for a local network. Do not include a trailing slash.</p>
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
  pendingConfig.wsUrl = server.arg("wsUrl");
  pendingConfig.wsToken = server.arg("wsToken");

  // Strip trailing slash if present.
  if (pendingConfig.wsUrl.endsWith("/"))
    pendingConfig.wsUrl.remove(pendingConfig.wsUrl.length() - 1);

  saveConfig(pendingConfig);
  server.send_P(200, "text/html", SAVED_HTML);
  configReceived = true;
}

// Blocks until the user submits the setup form, then returns.
void runSetupMode() {
  Serial.printf("Setup mode: AP \"%s\"\n", AP_SSID);

  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASSWORD);

  server.on("/", HTTP_GET, handleRoot);
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
  return Ping.ping(IPAddress(8, 8, 8, 8), 3) ||
         Ping.ping(IPAddress(1, 1, 1, 1), 3);
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
    sendState();
  } else if (event == WebsocketsEvent::ConnectionClosed) {
    Serial.printf("WebSocket disconnected. Reason: %s\n",
                  data.isEmpty() ? "(no reason given)" : data.c_str());
  } else if (event == WebsocketsEvent::GotPing) {
    wsClient.pong();
  }
}

bool connectWS() {
  if (currentConfig.wsUrl.isEmpty() || currentConfig.wsToken.isEmpty()) {
    Serial.println("No WebSocket config - skipping");
    return false;
  }

  wsClient.onMessage(onWsMessage);
  wsClient.onEvent(onWsEvent);

  // Parse wsUrl into components so we can use the host/port/path overloads,
  // which are more reliable than passing a full URL string to the library.
  bool useTls = currentConfig.wsUrl.startsWith("wss://");
  String hostPart =
      currentConfig.wsUrl.substring(useTls ? 6 : 5); // strip scheme
  String host;
  int port;
  int colonIdx = hostPart.indexOf(':');
  if (colonIdx >= 0) {
    host = hostPart.substring(0, colonIdx);
    port = hostPart.substring(colonIdx + 1).toInt();
  } else {
    host = hostPart;
    port = useTls ? 443 : 80;
  }
  String path = "/ws/esp?token=" + currentConfig.wsToken;

  Serial.printf("Connecting to %s://%s:%d%s\n", useTls ? "wss" : "ws",
                host.c_str(), port, path.c_str());

  bool ok;
  if (useTls) {
    wsClient.setInsecure();
    ok = wsClient.connectSecure(host, port, path);
  } else {
    ok = wsClient.connect(host, port, path);
  }

  if (!ok)
    Serial.println("WebSocket connection failed");
  return ok;
}

// --- setup / loop ------------------------------------------------------------
void setup() {
  Serial.begin(115200);

  checkFactoryReset();

  pinMode(MOTOR_PIN1, OUTPUT);
  pinMode(MOTOR_PIN2, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  ledcAttachChannel(ENABLE_PIN, PWM_FREQ, PWM_RESOLUTION, PWM_CHANNEL);

  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  ledcWrite(ENABLE_PIN, 0);
  doorState = loadDoorState();

  while (true) {
    currentConfig = loadConfig();
    if (connectWiFi(currentConfig))
      break;
    runSetupMode();
  }

  if (hasInternet())
    connectWS();
  else
    Serial.println("No internet - WebSocket skipped");
}

// Exponential backoff state for WebSocket reconnection
unsigned long wsNextRetryMs = 0;
unsigned long wsRetryDelayMs = 2000;
const unsigned long WS_RETRY_MAX_MS = 60000;

void loop() {
  if (!currentConfig.wsUrl.isEmpty() && !wsClient.available()) {
    unsigned long now = millis();
    if (now >= wsNextRetryMs) {
      if (connectWS()) {
        wsRetryDelayMs = 2000;
      } else {
        wsRetryDelayMs = min(wsRetryDelayMs * 2, WS_RETRY_MAX_MS);
      }
      wsNextRetryMs = millis() + wsRetryDelayMs;
    }
  }
  wsClient.poll();
}
