# Garage Door Remote Control — System Documentation

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Component Breakdown](#3-component-breakdown)
   - [Backend (FastAPI)](#31-backend-fastapi)
   - [Embedded Firmware (ESP32)](#32-embedded-firmware-esp32)
   - [Web Frontend](#33-web-frontend)
   - [Nginx Reverse Proxy](#34-nginx-reverse-proxy)
4. [Communication Protocols](#4-communication-protocols)
5. [API Reference](#5-api-reference)
6. [Authentication & Security](#6-authentication--security)
7. [Configuration & Environment Variables](#7-configuration--environment-variables)
8. [Setup & Deployment Guide](#8-setup--deployment-guide)
   - [Backend](#81-backend)
   - [ESP32 First-Boot Setup](#82-esp32-first-boot-setup)
   - [Nginx (Production)](#83-nginx-production)
9. [State Machine](#9-state-machine)
10. [Data Flow Diagrams](#10-data-flow-diagrams)
11. [Security Considerations](#11-security-considerations)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Project Overview

A remote-controlled garage door system built on three main layers:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python / FastAPI | Control hub, auth, state broker |
| Embedded | ESP32 / Arduino (C++) | Motor driver, WiFi + WebSocket client |
| Frontend | Vanilla HTML/JS | Browser control panel |

**Core design constraints:**
- No door position sensors (reed switches, etc.). The system infers door state from command history and persists it to ESP32 flash.
- Commands are fire-and-forget. There is no acknowledgement loop beyond the motor running for a fixed 2-second duration.
- A single shared WebSocket connection carries all bidirectional communication between the backend and the ESP32.

---

## 2. System Architecture

```
┌─────────────────────────────────────────┐
│          Browser / Mobile Client         │
│  (login.html → index.html)              │
└────────────────┬────────────────────────┘
                 │  HTTPS + WSS (JWT Bearer)
                 ▼
┌─────────────────────────────────────────┐
│              Nginx                       │
│  TLS termination, reverse proxy         │
│  garagedoor.amai.bg:443                 │
└────────────────┬────────────────────────┘
                 │  HTTP + WS (localhost:8000)
                 ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                  │
│  auth.py   door.py   state.py           │
│  ws_manager.py  (ESP32Manager)          │
└────────────────┬────────────────────────┘
                 │  WSS /ws/esp (shared token)
                 ▼
┌─────────────────────────────────────────┐
│              ESP32                       │
│  GarageDoor.ino                         │
│  Motor driver (L298N or similar)        │
└────────────────┬────────────────────────┘
                 │  GPIO pins 26, 27, 14
                 ▼
┌─────────────────────────────────────────┐
│          Garage Door Motor               │
└─────────────────────────────────────────┘
```

---

## 3. Component Breakdown

### 3.1 Backend (FastAPI)

Located in `backend/`.

#### Files

| File | Responsibility |
|------|----------------|
| `main.py` | App factory, router registration, HTML routes, WebSocket endpoints |
| `config.py` | `Settings` model — loads secrets from `.env` via `pydantic-settings` |
| `auth.py` | JWT login endpoint, `require_auth` FastAPI dependency |
| `door.py` | `POST /door/trigger` — sends command to ESP32 via WebSocket |
| `state.py` | `GET /door/state` — returns last known door and motor state |
| `ws_manager.py` | `ESP32Manager` singleton — owns ESP32 WS connection and UI client registry |

#### Key module: `ESP32Manager` (`ws_manager.py`)

The singleton `manager` object is the central state store:

```
ESP32Manager
├── _ws              — active WebSocket to the ESP32 (or None)
├── _door_state      — "open" | "closed" | "unknown"
├── _motor_state     — "idle" | "moving"
└── _ui_clients[]    — list of connected browser WebSockets
```

On every state change (ESP32 sends a message, or the ESP32 connects/disconnects), `_broadcast()` pushes the current payload to all UI clients:

```json
{
  "door": "open | closed | unknown",
  "motor": "idle | moving",
  "esp_connected": true | false
}
```

---

### 3.2 Embedded Firmware (ESP32)

Located in `embedded/GarageDoor/GarageDoor.ino`.

**Language:** C++ (Arduino framework)

**Required libraries** (install via Arduino Library Manager):
- `ArduinoWebsockets` — Gil Maimon
- `ArduinoJson` — Benoit Blanchon
- `ESP32Ping` — marian-craciunescu

#### Pin assignment

| Pin | Role |
|-----|------|
| GPIO 27 (`MOTOR_PIN1`) | H-bridge direction 1 |
| GPIO 26 (`MOTOR_PIN2`) | H-bridge direction 2 |
| GPIO 14 (`ENABLE_PIN`) | PWM enable signal |

**PWM:** 30 kHz, 8-bit resolution, duty cycle 200/255 (~78%).

#### Motor logic

```
doorState == "closed"  →  FORWARD  (PIN2=HIGH, PIN1=LOW)  →  nextState = "open"
doorState == "open"    →  BACKWARD (PIN1=HIGH, PIN2=LOW)  →  nextState = "closed"
doorState == "unknown" →  FORWARD                          →  nextState = "unknown"
```

Motor runs for **2 000 ms** (hardcoded `delay(2000)` in `triggerMotor()`), then stops. While running, any further `trigger` commands are silently ignored (`motorBusy` flag).

#### Configuration storage (NVS flash)

Credentials are stored in the `garage` NVS namespace using the ESP32 `Preferences` library. Keys:

| Key | Type | Description |
|-----|------|-------------|
| `ssid` | String | WiFi network name |
| `wifiPass` | String | WiFi password |
| `wsHost` | String | Backend hostname or IP |
| `wsPort` | Int | Backend port (443 = TLS, 8000 = plain) |
| `wsToken` | String | Shared secret, must match `ESP_WS_TOKEN` |
| `door` | String | Persisted door state across reboots |

#### Boot sequence

```
1. Initialize GPIO / PWM
2. Load persisted door state from NVS
3. Load WiFi config from NVS
4. Attempt WiFi connection (15 s timeout)
   └─ On failure: launch captive portal (AP "GarageDoor-Setup")
      wait for user to submit form, then retry
5. Ping 8.8.8.8 / 1.1.1.1 to verify internet
6. Connect to backend via WebSocket
7. Send current door + motor state
```

#### WebSocket reconnection (loop)

Uses exponential back-off: starts at 2 s, doubles on each failure, caps at 60 s. Resets to 2 s on successful reconnection.

#### First-boot captive portal

If stored WiFi credentials are missing or connection fails, the ESP32 starts an access point:

- **SSID:** `GarageDoor-Setup`
- **Password:** `setup1234`
- **URL:** `http://192.168.4.1` (default SoftAP IP)

The portal form accepts: WiFi SSID, WiFi password, backend host, port, and device token. After submission the credentials are saved to NVS and the AP is shut down.

---

### 3.3 Web Frontend

Located in `backend/frontend/`.

| File | Route | Description |
|------|-------|-------------|
| `login.html` | `GET /login` | Username / password form. Posts to `POST /auth/login`, stores JWT in `localStorage`. |
| `index.html` | `GET /` | Control panel. Requires JWT. Connects to `/ws/ui` for live state. |

The control panel UI elements:

- **ESP dot** — green when `esp_connected = true`, red otherwise.
- **Door badge** — `Open` (green), `Closed` (red), `Unknown` (grey).
- **Motor badge** — `Idle` (grey), `Moving…` (amber).
- **Trigger button** — disabled when ESP is offline or motor is moving. Label changes: `Open` / `Close` / `Trigger` based on current door state.

The frontend reconnects the UI WebSocket automatically with exponential back-off (1 s → 30 s max).

---

### 3.4 Nginx Reverse Proxy

Located in `nginx/garagedoor.conf`.

**Responsibilities:**
- TLS termination (Let's Encrypt certificates via Certbot)
- HTTP → HTTPS redirect
- Proxy all traffic to `127.0.0.1:8000`
- Extended WebSocket timeouts for `/ws/esp` (3600 s read/send) to keep the persistent ESP32 connection alive

**Installation:**
```bash
sudo cp nginx/garagedoor.conf /etc/nginx/sites-available/garagedoor
sudo ln -s /etc/nginx/sites-available/garagedoor /etc/nginx/sites-enabled/garagedoor
sudo certbot --nginx -d garagedoor.amai.bg
sudo nginx -t && sudo systemctl reload nginx
```

---

## 4. Communication Protocols

### 4.1 Browser ↔ Backend

| Direction | Protocol | Auth | Description |
|-----------|----------|------|-------------|
| Browser → Backend | HTTPS REST | JWT Bearer | Login, trigger command |
| Backend → Browser | WSS `/ws/ui?token=<jwt>` | JWT query param | Live state push |

### 4.2 Backend ↔ ESP32

| Direction | Protocol | Auth | Description |
|-----------|----------|------|-------------|
| ESP32 → Backend | WSS `/ws/esp?token=<token>` | Shared token | Connect, send state updates |
| Backend → ESP32 | WSS (same connection) | — | Send `{"action": "trigger"}` |

#### Messages: Backend → ESP32

```json
{ "action": "trigger" }
```

#### Messages: ESP32 → Backend

Sent on connect, before and after motor run:

```json
{
  "door": "open | closed | unknown",
  "motor": "idle | moving"
}
```

---

## 5. API Reference

All endpoints except `POST /auth/login`, `GET /`, and `GET /login` require a JWT Bearer token.

### Authentication

#### `POST /auth/login`

**Body:**
```json
{ "username": "admin", "password": "changeme" }
```

**Response 200:**
```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

**Response 401:** Invalid credentials.

---

### Door Control

#### `POST /door/trigger`

Sends `{"action": "trigger"}` to the ESP32 over WebSocket.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{ "status": "command sent" }
```

**Response 503:** ESP32 not connected.

**Response 409:** Motor is already running.

---

### Door State

#### `GET /door/state`

Returns the last known state as reported by the ESP32.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "door": "open | closed | unknown",
  "motor": "idle | moving",
  "esp_connected": true
}
```

---

### WebSocket Endpoints

#### `GET /ws/esp?token=<esp_ws_token>`

Persistent connection for the ESP32. Authenticated by the shared `ESP_WS_TOKEN` secret. Invalid token closes with code `1008` (Policy Violation).

#### `GET /ws/ui?token=<jwt>`

Live state subscription for browser clients. Authenticated by JWT. On connect, the current state is pushed immediately. The browser does not send messages over this connection.

---

### Static Pages

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves `frontend/index.html` |
| `GET` | `/login` | Serves `frontend/login.html` |

---

## 6. Authentication & Security

### JWT Tokens

- Algorithm: **HS256**
- Expiry: **24 hours**
- Secret: `JWT_SECRET_KEY` from `.env` — must be a long random string
- The token is stored in browser `localStorage` and sent as a `Bearer` header on every API call and as a query parameter when opening the UI WebSocket

### ESP32 Token

- A separate static shared secret (`ESP_WS_TOKEN`) authenticates the ESP32 connection
- It is stored in the ESP32's NVS flash under the key `wsToken`
- Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

### TLS

- Production: Nginx terminates TLS using Let's Encrypt certificates
- The ESP32 connects over `wss://` and calls `setInsecure()` (skips CA verification) — the shared token still ensures only the provisioned device can connect
- Local dev: plain `ws://` on port 8000 is acceptable

### Security Headers (Nginx)

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
```

---

## 7. Configuration & Environment Variables

Backend secrets are loaded from `backend/.env` (never committed):

```bash
# Copy the example and fill in values
cp backend/.env.example backend/.env
```

| Variable | Description | Example |
|----------|-------------|---------|
| `LOGIN_USERNAME` | Web UI username | `admin` |
| `LOGIN_PASSWORD` | Web UI password | `s3cur3pass` |
| `JWT_SECRET_KEY` | JWT signing secret (32+ random bytes) | `a1b2c3...` |
| `ESP_WS_TOKEN` | Shared token for ESP32 WebSocket auth | `d4e5f6...` |

Generate secrets:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 8. Setup & Deployment Guide

### 8.1 Backend

```bash
cd backend

# Create virtualenv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure secrets
cp .env.example .env
# Edit .env with your values

# Run (development)
uvicorn main:app --reload --port 8000

# Run (production, bound to localhost only — Nginx proxies it)
uvicorn main:app --host 127.0.0.1 --port 8000
```

**Code quality:**
```bash
ruff check .
ruff format .
```

---

### 8.2 ESP32 First-Boot Setup

1. Flash `embedded/GarageDoor/GarageDoor.ino` via Arduino IDE (select board: **ESP32 Dev Module**).
2. Power on the ESP32. On first boot (no credentials in NVS) it starts an access point.
3. On your phone or laptop, connect to WiFi network **`GarageDoor-Setup`** (password: `setup1234`).
4. Open a browser and navigate to `http://192.168.4.1`.
5. Fill in the setup form:
   - **SSID / Password** — your home WiFi
   - **Hostname / IP** — your backend (e.g. `garagedoor.amai.bg` or `192.168.1.50`)
   - **Port** — `443` for production, `8000` for local
   - **Device token** — the value of `ESP_WS_TOKEN` from your backend `.env`
6. Submit. The ESP32 saves credentials to NVS, shuts down the AP, and connects.

**Subsequent reboots** skip the portal and connect automatically.

**Serial monitor** (115200 baud) shows connection progress and state changes.

---

### 8.3 Nginx (Production)

```bash
# Copy config
sudo cp nginx/garagedoor.conf /etc/nginx/sites-available/garagedoor
sudo ln -s /etc/nginx/sites-available/garagedoor /etc/nginx/sites-enabled/garagedoor

# Obtain TLS certificate
sudo certbot --nginx -d garagedoor.amai.bg

# Validate and reload
sudo nginx -t && sudo systemctl reload nginx
```

Ensure your FastAPI server is running on `127.0.0.1:8000` before enabling the site.

---

## 9. State Machine

### Door State

```
          trigger (was closed)
 closed ─────────────────────► open
   ▲                             │
   │     trigger (was open)      │
   └─────────────────────────────┘

 unknown ──► FORWARD run ──► unknown
```

State is persisted to ESP32 NVS after each motor run. On boot, `"unknown"` in NVS is treated as `"closed"` (safe default).

### Motor State

```
  idle ──► [trigger received] ──► moving ──► [2000 ms elapsed] ──► idle
```

The motor cannot be re-triggered while `moving`. The backend enforces this at the API layer (`409 Conflict`) and the ESP32 enforces it locally (`motorBusy` flag).

---

## 10. Data Flow Diagrams

### Trigger Flow (happy path)

```
Browser          Backend          ESP32
  │                │                │
  │─ POST /door/trigger ──────────► │
  │  (Bearer token)                 │
  │                │                │
  │                │─ {"action":"trigger"} ─►│
  │                │                │
  │◄─ 200 OK ──────│                │
  │                │                │
  │                │◄─ {"door":"open","motor":"moving"} ─│
  │                │                │
  │◄─ WS push ─────│  (broadcast)   │
  │  (door+motor)  │                │
  │                │   [2000 ms]    │
  │                │                │
  │                │◄─ {"door":"open","motor":"idle"} ─│
  │                │                │
  │◄─ WS push ─────│  (broadcast)   │
```

### ESP32 Reconnection Flow

```
ESP32                            Backend
  │                                 │
  │── wss://.../ws/esp?token=... ──►│
  │                                 │── validates token
  │                                 │── accepts connection
  │◄──────────────────────────── 101 Upgrade ──│
  │                                 │
  │── {"door":"closed","motor":"idle"} ───────►│
  │                                 │── broadcasts to UI clients
```

---

## 11. Security Considerations

| Risk | Mitigation |
|------|-----------|
| Exposed JWT secret | Loaded from `.env`, never committed |
| Brute-force login | Single-user system; consider rate limiting for production |
| ESP32 impersonation | Shared `ESP_WS_TOKEN` required; rotate if compromised |
| TLS certificate | Let's Encrypt via Certbot (auto-renews) |
| Unencrypted local traffic | Backend binds to `127.0.0.1`; only Nginx is public-facing |
| NVS token exposure | Requires physical device access; acceptable for home use |
| Replay attacks | JWT expiry (24 h); ESP token is long-lived — physical security of device assumed |

**Secrets that must never be committed:**
```
backend/.env
embedded/config.json   (if MicroPython version is used)
*.pem
*.key
```

---

## 12. Troubleshooting

### ESP32 stuck in setup mode

The ESP32 falls back to setup mode when WiFi connection fails after 15 seconds. Check:
- SSID and password are correct (case-sensitive)
- The ESP32 is within range of the access point
- Open the serial monitor (115200 baud) for diagnostic output

### Backend returns `503 ESP32 is not connected`

The `ESP32Manager._ws` is `None`. Check:
- ESP32 serial output for WebSocket connection errors
- `wsHost`, `wsPort`, and `wsToken` stored in NVS match the backend `.env`
- Nginx is running and forwarding `/ws/esp` correctly (check `proxy_read_timeout`)

### JWT expired / `401 Unauthorized`

Tokens expire after 24 hours. The browser will redirect to `/login` automatically when a `401` is received on a trigger request.

### Motor runs but door state is wrong

The system infers door state — it has no sensors. If the state gets out of sync (e.g. manual door operation, power loss mid-run), trigger once to move the door, then verify visually and trigger again if needed. The state will follow subsequent commands correctly.

### WebSocket UI disconnects frequently

The UI WebSocket reconnects automatically with exponential back-off (1 s → 30 s). If disconnects are persistent:
- Check Nginx `proxy_read_timeout` for `/ws/ui` (default 60 s may time out idle connections — consider increasing or adding WebSocket keep-alive pings)
- Verify the JWT has not expired (stale token causes `1008` close on reconnect)
