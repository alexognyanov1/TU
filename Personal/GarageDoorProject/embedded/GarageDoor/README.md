# GarageDoor firmware — BLE edition

Direct Bluetooth Low Energy control. No WiFi, no backend, no cloud.
Paired from a web page via the Web Bluetooth API.

## 1. Arduino setup

- **Board:** ESP32 Dev Module (or whichever matches your devkit).
- **Core:** ESP32 Arduino core **v3.x** (required for `ledcAttachChannel` and NimBLE 2.x).
- **Library:** **NimBLE-Arduino** by **h2zero**, version **2.2.x** or newer. Install via Library Manager.
  - The firmware uses the v2 callback signatures (`onWrite(chr, connInfo)`). It will **not** compile against NimBLE v1.x.

That is the only third-party library. No ArduinoJson, no WebSocket, no Ping — all removed.

## 2. Hardware wiring

Unchanged from the previous revision:

| Signal | GPIO | Notes |
|---|---|---|
| Motor direction 1 | 27 | H-bridge input 1 |
| Motor direction 2 | 26 | H-bridge input 2 |
| Motor PWM / enable | 14 | H-bridge enable, 30 kHz PWM |
| Reset button | 0 | Uses onboard BOOT; short to GND for 3 s to clear NVS + bonds |
| Status LED | 2 | Onboard LED on most devkits; used for connect/auth feedback |

**Power:** run the motor off its own rail, not from the laptop USB. Motor start can brown out the ESP32 and cause a mid-demo reboot. Use a 5V/2A supply (or higher per motor spec) for the motor and a separate USB or 5V supply for the ESP32 logic.

## 3. Configuration

Everything that needs changing lives at the top of `GarageDoor.ino`:

- `GARAGE_PASSWORD` — the app-layer BLE password. Must match the `DEFAULT_PASSWORD` constant in `frontend/ble.html`.
- `SERVICE_UUID` / `AUTH_UUID` / `CMD_UUID` / `STATE_UUID` / `INFO_UUID` — 128-bit GATT UUIDs. The placeholders in the file are fine for a demo. If you want each device in a fleet to be unique, regenerate all five with `uuidgen` (macOS) or `python -c "import uuid; print(uuid.uuid4())"` and copy them into both the firmware and `ble.html`.
- `MAX_AUTH_ATTEMPTS` — failed-password threshold before the device disconnects the client. Default 5.

After changing the password:
1. Edit `GARAGE_PASSWORD` in `GarageDoor.ino` → reflash.
2. Edit `DEFAULT_PASSWORD` in `frontend/ble.html` (and `docs/ble.html`) → redeploy the page.

## 4. Flashing

```
arduino-cli compile --fqbn esp32:esp32:esp32 embedded/GarageDoor
arduino-cli upload --fqbn esp32:esp32:esp32 -p /dev/cu.usbserial-XXXX embedded/GarageDoor
```

Or use the Arduino IDE: open `GarageDoor.ino`, select the ESP32 board and serial port, click Upload.

After flashing, open the serial monitor at 115200 baud. You should see:

```
Door state loaded: closed
Starting BLE as 'GarageDoor-ABCD'
BLE advertising started. Waiting for a client...
```

## 5. Hosting the web page

`frontend/ble.html` is a single self-contained HTML file with no build step and no external assets. Web Bluetooth requires a **secure context** (HTTPS or localhost), so pick one of these:

| Option | Good for | How |
|---|---|---|
| **Netlify Drop** | Fastest demo setup | https://app.netlify.com/drop → drag `ble.html` → get an `https://…netlify.app` URL in seconds. No account required. |
| **GitHub Pages** | Stable, free, versioned | Put the file in a `/docs` folder at your repo root (or on a `gh-pages` branch), enable Pages in repo Settings. URL: `https://<user>.github.io/<repo>/ble.html`. |
| **Cloudflare Pages / Vercel** | Nicer CI integration | Connect repo, auto-deploys on push. |
| **Local laptop, localhost only** | Demoing from the laptop itself (no phone) | `python3 -m http.server 8000` from the `frontend/` folder, open `http://localhost:8000/ble.html` in Chrome/Edge. Works because `localhost` is a secure context by browser rule. **Does NOT work for iPhone/Android over LAN** — HTTP on a LAN IP is not a secure context. |

For an iPhone demo, install **Bluefy — Web BLE Browser** (free, App Store) and open the HTTPS URL there. Safari and iOS Chrome do not implement Web Bluetooth.

## 6. Demo flow

1. Power on the ESP32. Serial prints `Advertising`.
2. Open the hosted `ble.html` in Chrome (laptop/Android) or Bluefy (iPhone).
3. Click **Connect**. Native picker appears listing `GarageDoor-XXXX`. Pick it.
4. Page writes the password to Auth char. Within a second, state badges go live and **Auth=OK**.
5. Click the big Trigger button. Motor runs 2 s; badges flip Moving → Idle, door Open/Closed.
6. To re-demo the pairing flow:
   - Click **Forget device** in the web page (clears bonds on ESP, restarts it), **or**
   - Walk to the device and hold **BOOT** 3 s.
   - **Also** remove the device from your laptop/phone's OS-level Bluetooth list, or the next pairing will look partial:
     - macOS: System Settings → Bluetooth → (i) on the device → Forget Device
     - Windows: Settings → Bluetooth & devices → Remove device
     - Android: Bluetooth settings → gear icon → Forget
     - iOS: Settings → Bluetooth → (i) → Forget This Device
7. Click **Connect** again. The picker re-appears from zero.

## 7. Security notes

- **"Just Works" link-layer pairing** means anyone in RF range can connect. This is intentional: Web Bluetooth hides the OS pairing UI from the page, so Passkey pairing would make the browser UX inconsistent across OSes. For the demo, we rely on the app-layer password.
- **App-layer password** is transmitted in plain text over the (unencrypted) BLE link. A Bluetooth sniffer in range can capture it. Acceptable for a demo; for production you would add bonded BLE + signed commands with a per-device secret.
- **Rate limiting:** 5 failed password writes on one connection → forced disconnect. Per-connection, so someone has to reconnect to try again. No IP-style lockout (there are no IPs in BLE).
- **Factory reset via BOOT button** clears NVS (door state) and NimBLE bond storage, then restarts.

## 8. Legacy WiFi code

The WiFi + WebSocket + captive-portal version lives in the git history. The FastAPI backend under `backend/` is the client half of that old setup and is currently unused — it's kept in the repo for reference.

## 9. Troubleshooting

- **"No matching devices" in picker:** ESP32 not advertising, too far away, or already connected to another central. Power-cycle the ESP32.
- **Connect works but Auth stays at "…":** Password mismatch between firmware and HTML. Check both match.
- **macOS Bluetooth flaky:** `sudo pkill bluetoothd` to restart the stack without rebooting.
- **2.4 GHz interference:** BLE and WiFi share the band. Turn off laptop WiFi during demo if it's acting up.
- **Motor doesn't move but serial says "Motor: closed -> open":** hardware issue — check H-bridge wiring, motor power, and that `ENABLE_PIN` PWM is actually reaching the driver.
- **`navigator.bluetooth is undefined`:** browser doesn't support Web Bluetooth. Use Chrome/Edge on desktop, Chrome on Android, or Bluefy on iOS.
