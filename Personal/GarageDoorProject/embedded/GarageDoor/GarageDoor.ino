// Required library (install via Arduino Library Manager):
//   NimBLE-Arduino  - h2zero  (tested with v2.2.x)
//
// Direct BLE control. No WiFi, no backend, no cloud.
// Pair via the Web Bluetooth page at frontend/ble.html (or the GitHub Pages copy).
//
// Security model:
//   - "Just Works" link-layer (no bonding, setSecurityAuth(false,false,false))
//   - App-layer password: client writes GARAGE_PASSWORD to Auth char after
//     connecting. Without that, commands are silently rejected.
//   - Per-connection auth flag. 5 bad attempts -> disconnect.

#include <Arduino.h>
#include <NimBLEDevice.h>
#include <Preferences.h>
#include <map>

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

// --- Reset button ------------------------------------------------------------
// Wire a push button between this pin and GND (or use the onboard BOOT button).
// Hold during/after power-on for 3 s to clear all stored data and bonds.
const int RESET_BTN_PIN = 0;
const int RESET_HOLD_MS = 3000;

// --- Onboard LED (demo feedback) ---------------------------------------------
const int LED_PIN = 2;

// --- BLE UUIDs (regenerate with `uuidgen` for unique devices) ----------------
#define SERVICE_UUID "6a4e3200-667b-11ee-b962-0242ac120002"
#define AUTH_UUID    "6a4e3201-667b-11ee-b962-0242ac120002"
#define CMD_UUID     "6a4e3202-667b-11ee-b962-0242ac120002"
#define STATE_UUID   "6a4e3203-667b-11ee-b962-0242ac120002"
#define INFO_UUID    "6a4e3204-667b-11ee-b962-0242ac120002"

// --- Hardcoded BLE password --------------------------------------------------
// CHANGE THIS to rotate. The same string must be set in the GARAGE_PASSWORD
// constant in frontend/ble.html. Reflash + redeploy the page after changing.
#define GARAGE_PASSWORD "garage-demo-2026"

const int MAX_AUTH_ATTEMPTS = 5;

// --- Globals -----------------------------------------------------------------
Preferences prefs;

String doorState = "unknown"; // persisted: "open", "closed", "unknown"
bool motorBusy = false;

NimBLEServer* bleServer = nullptr;
NimBLECharacteristic* stateChar = nullptr;

struct ConnState {
  bool authed = false;
  uint8_t authAttempts = 0;
};
std::map<uint16_t, ConnState> conns;

volatile bool pendingClearBonds = false;
volatile bool pendingTrigger = false;

// --- Factory reset -----------------------------------------------------------
void checkFactoryReset() {
  pinMode(RESET_BTN_PIN, INPUT_PULLUP);

  if (digitalRead(RESET_BTN_PIN) != LOW)
    return;

  Serial.println("Reset button held - hold for 3 s to clear all data...");

  unsigned long start = millis();
  while (digitalRead(RESET_BTN_PIN) == LOW) {
    if (millis() - start >= RESET_HOLD_MS) {
      Serial.println("Clearing NVS and BLE bonds...");
      prefs.begin("garage", false);
      prefs.clear();
      prefs.end();
      // Temporarily bring up NimBLE so we can purge its bond storage in NVS.
      NimBLEDevice::init("");
      NimBLEDevice::deleteAllBonds();
      NimBLEDevice::deinit(true);
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

// --- State broadcasting ------------------------------------------------------
static void sendStateTo(uint16_t connHandle, bool authed) {
  if (!stateChar)
    return;
  char json[128];
  snprintf(json, sizeof(json),
           "{\"door\":\"%s\",\"motor\":\"%s\",\"authed\":%s}",
           doorState.c_str(),
           motorBusy ? "moving" : "idle",
           authed ? "true" : "false");
  stateChar->setValue((uint8_t *)json, strlen(json));
  stateChar->notify(connHandle);
}

// Per-subscriber broadcast (each client sees its own authed flag).
void sendState() {
  if (!stateChar)
    return;

  char generic[96];
  snprintf(generic, sizeof(generic),
           "{\"door\":\"%s\",\"motor\":\"%s\"}",
           doorState.c_str(),
           motorBusy ? "moving" : "idle");
  stateChar->setValue((uint8_t *)generic, strlen(generic));

  for (auto &p : conns) {
    sendStateTo(p.first, p.second.authed);
  }
  Serial.printf("State: door=%s motor=%s subscribers=%u\n",
                doorState.c_str(), motorBusy ? "moving" : "idle",
                (unsigned)conns.size());
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

// --- Auth helpers ------------------------------------------------------------
static bool constantTimeEquals(const uint8_t *a, size_t alen, const char *b) {
  size_t blen = strlen(b);
  if (alen != blen)
    return false;
  uint8_t diff = 0;
  for (size_t i = 0; i < alen; i++)
    diff |= a[i] ^ (uint8_t)b[i];
  return diff == 0;
}

// --- BLE callbacks -----------------------------------------------------------
class ServerCallback : public NimBLEServerCallbacks {
  void onConnect(NimBLEServer *pServer, NimBLEConnInfo &connInfo) override {
    uint16_t h = connInfo.getConnHandle();
    conns[h] = ConnState{};
    digitalWrite(LED_PIN, HIGH);
    Serial.printf("[BLE] Client connected: conn=%u\n", h);
  }

  void onDisconnect(NimBLEServer *pServer, NimBLEConnInfo &connInfo,
                    int reason) override {
    uint16_t h = connInfo.getConnHandle();
    conns.erase(h);
    if (conns.empty())
      digitalWrite(LED_PIN, LOW);
    Serial.printf("[BLE] Client disconnected: conn=%u reason=%d\n", h, reason);
    NimBLEDevice::startAdvertising();
  }
};

class AuthCallback : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic *pChr,
               NimBLEConnInfo &connInfo) override {
    uint16_t h = connInfo.getConnHandle();
    auto it = conns.find(h);
    if (it == conns.end())
      return;

    std::string v = pChr->getValue();
    bool ok = constantTimeEquals((const uint8_t *)v.data(), v.size(),
                                 GARAGE_PASSWORD);

    if (ok) {
      it->second.authed = true;
      it->second.authAttempts = 0;
      Serial.printf("[BLE] Auth success conn=%u\n", h);
      sendStateTo(h, true);
      // 4 quick blinks = authed OK
      for (int i = 0; i < 4; i++) {
        digitalWrite(LED_PIN, LOW);
        delay(70);
        digitalWrite(LED_PIN, HIGH);
        delay(70);
      }
    } else {
      it->second.authAttempts++;
      Serial.printf("[BLE] Auth failed conn=%u attempts=%u\n", h,
                    it->second.authAttempts);
      sendStateTo(h, false);
      if (it->second.authAttempts >= MAX_AUTH_ATTEMPTS) {
        Serial.printf("[BLE] Disconnecting conn=%u after %d failures\n", h,
                      MAX_AUTH_ATTEMPTS);
        bleServer->disconnect(h);
      }
    }
  }
};

class CommandCallback : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic *pChr,
               NimBLEConnInfo &connInfo) override {
    uint16_t h = connInfo.getConnHandle();
    auto it = conns.find(h);
    if (it == conns.end() || !it->second.authed) {
      Serial.printf("[BLE] Command from unauthed conn=%u -- rejected\n", h);
      return;
    }
    std::string cmd = pChr->getValue();
    Serial.printf("[BLE] Command: %s\n", cmd.c_str());

    if (cmd == "trigger") {
      // Defer the motor run to loop() so the 2 s blocking delay doesn't
      // stall the BLE host task and hold up the write response.
      if (motorBusy) {
        Serial.println("[BLE] Motor busy - ignoring trigger");
      } else {
        pendingTrigger = true;
      }
    } else if (cmd == "clear_bonds") {
      Serial.println("[BLE] clear_bonds requested - deferring to loop()");
      pendingClearBonds = true;
    } else {
      Serial.printf("[BLE] Unknown command: %s\n", cmd.c_str());
    }
  }
};

// --- Device name from chip MAC ----------------------------------------------
static String makeDeviceName() {
  uint64_t mac = ESP.getEfuseMac();
  char buf[24];
  snprintf(buf, sizeof(buf), "GarageDoor-%04X", (uint16_t)(mac >> 32));
  return String(buf);
}

// --- setup / loop ------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(100);

  checkFactoryReset();

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  pinMode(MOTOR_PIN1, OUTPUT);
  pinMode(MOTOR_PIN2, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  ledcAttachChannel(ENABLE_PIN, PWM_FREQ, PWM_RESOLUTION, PWM_CHANNEL);

  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  ledcWrite(ENABLE_PIN, 0);

  doorState = loadDoorState();
  Serial.printf("Door state loaded: %s\n", doorState.c_str());

  String name = makeDeviceName();
  Serial.printf("Starting BLE as '%s'\n", name.c_str());

  NimBLEDevice::init(name.c_str());
  NimBLEDevice::setSecurityAuth(false, false, false); // no bond / no MITM / no SC
  NimBLEDevice::setMTU(185);

  bleServer = NimBLEDevice::createServer();
  bleServer->setCallbacks(new ServerCallback());

  NimBLEService *svc = bleServer->createService(SERVICE_UUID);

  NimBLECharacteristic *authChar =
      svc->createCharacteristic(AUTH_UUID, NIMBLE_PROPERTY::WRITE);
  authChar->setCallbacks(new AuthCallback());

  NimBLECharacteristic *cmdChar =
      svc->createCharacteristic(CMD_UUID, NIMBLE_PROPERTY::WRITE);
  cmdChar->setCallbacks(new CommandCallback());

  stateChar = svc->createCharacteristic(
      STATE_UUID, NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY);

  NimBLECharacteristic *infoChar =
      svc->createCharacteristic(INFO_UUID, NIMBLE_PROPERTY::READ);
  char info[96];
  snprintf(info, sizeof(info),
           "{\"firmware\":\"1.0.0-ble\",\"name\":\"%s\"}", name.c_str());
  infoChar->setValue((uint8_t *)info, strlen(info));

  svc->start();

  // Seed the State char so a READ before the first Notify returns something.
  char initial[96];
  snprintf(initial, sizeof(initial),
           "{\"door\":\"%s\",\"motor\":\"idle\"}", doorState.c_str());
  stateChar->setValue((uint8_t *)initial, strlen(initial));

  // Flags (3B) + 128-bit service UUID (18B) + 15-char name (17B) = 38B, which
  // overflows the 31-byte advertising PDU. Split: service UUID in the main
  // packet, name in the scan response. Both fit comfortably under 31B each.
  NimBLEAdvertising *adv = NimBLEDevice::getAdvertising();

  NimBLEAdvertisementData advData;
  advData.setFlags(0x06); // LE General Discoverable + BR/EDR Not Supported
  advData.addServiceUUID(SERVICE_UUID);
  adv->setAdvertisementData(advData);

  NimBLEAdvertisementData scanData;
  scanData.setName(name.c_str());
  adv->setScanResponseData(scanData);

  adv->setMinInterval(0x20); // 20 ms
  adv->setMaxInterval(0x40); // 40 ms
  adv->start();

  Serial.println("BLE advertising started. Waiting for a client...");
}

void loop() {
  if (pendingClearBonds) {
    pendingClearBonds = false;
    Serial.println("[BLE] Clearing bonds and restarting...");
    for (auto &p : conns) {
      bleServer->disconnect(p.first);
    }
    delay(200);
    NimBLEDevice::deleteAllBonds();
    delay(300);
    ESP.restart();
  }
  if (pendingTrigger) {
    pendingTrigger = false;
    triggerMotor();
  }
  delay(20);
}
