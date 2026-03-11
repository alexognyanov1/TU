# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Remote-controlled garage door system with three components:
- **`embedded/`** — ESP32 firmware (MicroPython)
- **`backend/`** — Python FastAPI server acting as the control hub
- **`backend/frontend/`** — Static HTML pages served by FastAPI (`GET /` and `GET /login`)

Communication: ESP32 connects to the backend over MQTT or WebSocket. The backend exposes a REST API (and optionally a WebSocket endpoint) for a frontend or mobile client.

The ESP32's only job is to spin the garage door motor for a configured duration when it receives a command. There is no door state sensing, no reed switch, and no feedback loop — the backend treats each command as fire-and-forget.

## Architecture

```
[Mobile/Web Client]
        |
        v
[Python Backend (FastAPI)]
        |
     MQTT / WebSocket
        |
        v
[ESP32 Firmware]
        |
   GPIO relay pin
        |
        v
[Garage Door Motor]
```

### Key design decisions
- Authentication: the web frontend logs in via `POST /auth/login` (JSON body) and receives a JWT Bearer token, which is stored in `localStorage` and sent with every subsequent request.
- `POST /door/trigger` is the only door action — it publishes `{"action": "trigger"}` to the MQTT broker, which the ESP32 acts on.
- There is no door state — commands are fire-and-forget.
- Secrets are loaded from environment variables or a `.env` file (never committed).

## Backend (`backend/`)

### Stack
- Python 3.11+
- FastAPI + Uvicorn
- Paho-MQTT (or asyncio-mqtt) for broker communication
- Pydantic for config and request/response models

### Commands
```bash
cd backend

# Create and activate virtualenv
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and fill in secrets
cp .env.example .env

# Run dev server (auto-reload)
uvicorn main:app --reload --port 8000

# Lint / format
ruff check .
ruff format .
```

### Structure
- `main.py` — app factory, router registration, `GET /` and `GET /login` serve HTML from `frontend/`
- `config.py` — `Settings` loaded from `.env` via `pydantic-settings`
- `auth.py` — `POST /auth/login` → JWT; `require_auth` dependency used by other routes
- `door.py` — `POST /door/trigger` → publishes MQTT command

## Embedded (`embedded/`)

### Stack choice
Use **MicroPython** unless low-level peripheral timing requires C++. MicroPython is faster to iterate on and easier to maintain.

### File layout
```
embedded/
  main.py          # entry point, connects WiFi then starts event loop
  config.py        # loads secrets from config.json (not committed)
  mqtt_handler.py  # subscribe/publish logic
  motor_control.py # drives motor GPIO pin for a set duration
  config.json      # device secrets — add to .gitignore
```

### Flashing / development commands
```bash
# Install esptool and mpremote
pip install esptool mpremote

# Erase flash and write MicroPython firmware
esptool.py --port /dev/tty.usbserial-* erase_flash
esptool.py --port /dev/tty.usbserial-* write_flash -z 0x0 micropython-esp32.bin

# Upload files to the device
mpremote connect /dev/tty.usbserial-* cp embedded/main.py :main.py
mpremote connect /dev/tty.usbserial-* cp embedded/mqtt_handler.py :mqtt_handler.py

# Open REPL
mpremote connect /dev/tty.usbserial-*
```

### Best practices
- Store WiFi SSID/password and MQTT credentials in `config.json` on-device; load at boot via `ujson.load()`. Never hardcode credentials in source files.
- Use a **watchdog timer** (`machine.WDT`) so the device auto-resets on hang.
- Implement **reconnect logic** for both WiFi and MQTT with exponential backoff.
- On receiving a command, drive the motor GPIO pin HIGH for `MOTOR_RUN_DURATION_MS` (configured in `config.json`), then LOW. No state feedback is sent back.
- Ignore any new commands that arrive while the motor is already running.
- Use `uasyncio` for concurrent WiFi and MQTT handling; run the motor pulse as a non-blocking coroutine.

## Secrets & `.gitignore`

The following must never be committed:
```
.env
backend/.env
embedded/config.json
*.pem
*.key
```

Add all of the above to `.gitignore` at project root.

## MQTT Topic Schema

| Topic              | Publisher | Payload example                        |
|--------------------|-----------|----------------------------------------|
| `garage/command`   | Backend   | `{"action": "open"}`                   |
Use QoS 1 for commands to guarantee delivery. There is no status topic — the ESP32 does not publish state.
