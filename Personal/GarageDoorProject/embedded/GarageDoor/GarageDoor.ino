/**
 * GarageDoor.ino
 * ESP32 garage door controller — Arduino IDE
 *
 * Required libraries (install via Sketch → Include Library → Manage Libraries):
 *   - PubSubClient  by Nick O'Leary   (MQTT)
 *   - ArduinoJson   by Benoit Blanchon
 *
 * Setup:
 *   1. Copy config.h.example → config.h and fill in your credentials.
 *   2. Select board: "ESP32 Dev Module" (or your exact board variant).
 *   3. Upload.
 *
 * Door state machine (no physical sensor — purely time-based):
 *   closed  --[trigger]--> opening --[motor done]--> open
 *   open    --[trigger]--> closing --[motor done]--> closed
 *   A new trigger while the motor is running is silently ignored.
 */

#include "config.h"
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>

// ---------------------------------------------------------------------------
// Door state
// ---------------------------------------------------------------------------

enum DoorState { STATE_CLOSED, STATE_OPENING, STATE_OPEN, STATE_CLOSING };

const char *STATE_NAMES[] = {"closed", "opening", "open", "closing"};

DoorState doorState = STATE_CLOSED;

// ---------------------------------------------------------------------------
// Motor (non-blocking, driven by millis())
// ---------------------------------------------------------------------------

bool motorRunning = false;
unsigned long motorStartedAt = 0;

// ---------------------------------------------------------------------------
// MQTT
// ---------------------------------------------------------------------------

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

unsigned long lastReconnectAttempt = 0;
unsigned long reconnectDelay = 2000; // exponential backoff, max 60 s

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

void publishState(DoorState state) {
  char payload[48];
  StaticJsonDocument<48> doc;
  doc["state"] = STATE_NAMES[state];
  serializeJson(doc, payload, sizeof(payload));

  // retained=true so the backend receives the last known state on (re)connect
  mqtt.publish(MQTT_STATUS_TOPIC, payload, /*retained=*/true);
  Serial.printf("[door] state → %s\n", STATE_NAMES[state]);
}

void startMotor() {
  digitalWrite(MOTOR_PIN, HIGH);
  motorRunning = true;
  motorStartedAt = millis();
}

void stopMotor() {
  digitalWrite(MOTOR_PIN, LOW);
  motorRunning = false;

  // Advance to the final resting state
  doorState = (doorState == STATE_OPENING) ? STATE_OPEN : STATE_CLOSED;
  publishState(doorState);
}

void onTrigger() {
  if (motorRunning) {
    Serial.println("[door] motor already running — ignoring trigger");
    return;
  }

  if (doorState == STATE_CLOSED || doorState == STATE_CLOSING) {
    doorState = STATE_OPENING;
  } else {
    doorState = STATE_CLOSING;
  }

  publishState(doorState);
  startMotor();
}

// ---------------------------------------------------------------------------
// MQTT callback
// ---------------------------------------------------------------------------

void mqttCallback(char *topic, byte *payload, unsigned int length) {
  StaticJsonDocument<128> doc;
  DeserializationError err = deserializeJson(doc, payload, length);
  if (err) {
    Serial.printf("[mqtt] JSON parse error: %s\n", err.c_str());
    return;
  }

  const char *action = doc["action"];
  if (action && strcmp(action, "trigger") == 0) {
    onTrigger();
  }
}

// ---------------------------------------------------------------------------
// WiFi
// ---------------------------------------------------------------------------

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED)
    return;

  Serial.printf("[wifi] connecting to '%s'…\n", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - start > 20000) {
      Serial.println("[wifi] timeout — restarting");
      ESP.restart();
    }
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\n[wifi] connected: %s\n", WiFi.localIP().toString().c_str());
}

// ---------------------------------------------------------------------------
// MQTT reconnect (called from loop, non-blocking)
// ---------------------------------------------------------------------------

bool reconnectMQTT() {
  Serial.print("[mqtt] connecting…");

  bool ok;
  if (strlen(MQTT_USERNAME) > 0) {
    ok = mqtt.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD);
  } else {
    ok = mqtt.connect(MQTT_CLIENT_ID);
  }

  if (ok) {
    Serial.println(" connected");
    mqtt.subscribe(MQTT_COMMAND_TOPIC, /*qos=*/1);
    publishState(doorState); // let the backend know our current state
    reconnectDelay = 2000;   // reset backoff on success
  } else {
    Serial.printf(" failed (rc=%d) — retry in %lus\n", mqtt.state(),
                  reconnectDelay / 1000);
  }
  return ok;
}

// ---------------------------------------------------------------------------
// Arduino entry points
// ---------------------------------------------------------------------------

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("\n=== Garage Door Controller ===");

  pinMode(MOTOR_PIN, OUTPUT);
  digitalWrite(MOTOR_PIN, LOW);

  connectWiFi();

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
  mqtt.setBufferSize(512);

  reconnectMQTT();
}

void loop() {
  // --- WiFi watchdog ---
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[wifi] lost connection — reconnecting…");
    connectWiFi();
  }

  // --- MQTT keep-alive / reconnect with exponential backoff ---
  if (!mqtt.connected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt >= reconnectDelay) {
      lastReconnectAttempt = now;
      if (!reconnectMQTT()) {
        reconnectDelay = min(reconnectDelay * 2, (unsigned long)60000);
      }
    }
  } else {
    mqtt.loop(); // process incoming messages
  }

  // --- Motor timeout (non-blocking) ---
  if (motorRunning && millis() - motorStartedAt >= MOTOR_RUN_DURATION_MS) {
    stopMotor();
  }
}
