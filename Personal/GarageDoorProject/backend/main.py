import os

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

import auth
import door
import state as state_module
from auth import require_auth
from config import settings
from ws_manager import manager

app = FastAPI(title="Garage Door API")

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

app.include_router(auth.router)
app.include_router(door.router)
app.include_router(state_module.router)


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/login")
def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))


@app.websocket("/ws/esp")
async def esp_websocket(ws: WebSocket, token: str = Query(...)):
    """WebSocket endpoint for the ESP32. Authenticated by a shared token."""
    if token != settings.esp_ws_token:
        await ws.close(code=1008)  # Policy Violation
        return

    await ws.accept()
    await manager.set_ws(ws)
    print("[ws/esp] ESP32 connected")

    try:
        while True:
            data = await ws.receive_json()

            door_val  = data.get("door")
            motor_val = data.get("motor")

            valid_door  = {"open", "closed", "unknown"}
            valid_motor = {"idle", "moving"}

            await manager.update(
                door=door_val  if door_val  in valid_door  else None,
                motor=motor_val if motor_val in valid_motor else None,
            )
            print(f"[ws/esp] door={door_val} motor={motor_val}")

    except WebSocketDisconnect:
        print("[ws/esp] ESP32 disconnected")
    finally:
        await manager.set_ws(None)


@app.websocket("/ws/ui")
async def ui_websocket(ws: WebSocket, token: str = Query(...)):
    """WebSocket endpoint for browser clients. Authenticated by JWT Bearer token."""
    try:
        require_auth(token)
    except Exception:
        await ws.close(code=1008)
        return

    await ws.accept()
    await manager.add_ui_client(ws)
    print("[ws/ui] browser client connected")

    try:
        while True:
            # Keep the connection alive; browser does not send messages.
            await ws.receive_text()
    except WebSocketDisconnect:
        print("[ws/ui] browser client disconnected")
    finally:
        manager.remove_ui_client(ws)
