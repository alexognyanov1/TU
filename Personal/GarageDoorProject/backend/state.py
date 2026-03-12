"""Door state — subscribes to the MQTT status topic and exposes GET /door/state."""

import json
import threading

import paho.mqtt.client as mqtt_client
from fastapi import APIRouter, Depends

from auth import require_auth
from config import settings

router = APIRouter(prefix="/door", tags=["door"])

# In-memory door state. Updated by the MQTT subscriber thread.
_door_state: str = "unknown"
_state_lock = threading.Lock()


def get_door_state() -> str:
    with _state_lock:
        return _door_state


def _set_door_state(state: str):
    global _door_state
    with _state_lock:
        _door_state = state


# ---------------------------------------------------------------------------
# Background MQTT subscriber
# ---------------------------------------------------------------------------

def _on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe(settings.mqtt_status_topic, qos=1)
        print(f"[state] subscribed to {settings.mqtt_status_topic}")
    else:
        print(f"[state] MQTT connect failed, rc={rc}")


def _on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload)
        state = payload.get("state", "")
        if state in ("open", "opening", "closed", "closing"):
            _set_door_state(state)
            print(f"[state] door state updated: {state}")
    except Exception as e:
        print(f"[state] bad message: {e}")


def start_state_subscriber():
    """Starts a background thread that keeps the MQTT connection alive."""
    client = mqtt_client.Client(
        client_id="backend_state_subscriber",
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
    )
    if settings.mqtt_username:
        client.username_pw_set(settings.mqtt_username, settings.mqtt_password)
    if settings.mqtt_tls:
        client.tls_set()

    client.on_connect = _on_connect
    client.on_message = _on_message

    client.connect(settings.mqtt_broker, settings.mqtt_port, keepalive=60)

    thread = threading.Thread(target=client.loop_forever, daemon=True)
    thread.start()


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.get("/state")
def door_state_endpoint(_: str = Depends(require_auth)):
    """Returns the last known door state as reported by the ESP32."""
    return {"state": get_door_state()}
