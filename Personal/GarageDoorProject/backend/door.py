import json
import threading

import paho.mqtt.publish as mqtt_publish
from fastapi import APIRouter, Depends, HTTPException, status

from auth import require_auth
from config import settings

router = APIRouter(prefix="/door", tags=["door"])

PUBLISH_TIMEOUT_SECONDS = 5


def publish_command(action: str):
    """Publishes a command to the ESP32 over MQTT.

    Runs the blocking paho call in a background thread so the request is not
    held open indefinitely if the broker is unreachable. Raises an HTTP error
    if the publish does not complete within PUBLISH_TIMEOUT_SECONDS.
    """
    payload = json.dumps({"action": action})
    auth = {"username": settings.mqtt_username, "password": settings.mqtt_password} if settings.mqtt_username else None
    # paho expects an empty dict to enable TLS with default CA verification.
    tls = {} if settings.mqtt_tls else None

    error: list[Exception] = []

    def _publish():
        try:
            mqtt_publish.single(
                topic=settings.mqtt_command_topic,
                payload=payload,
                hostname=settings.mqtt_broker,
                port=settings.mqtt_port,
                auth=auth,
                transport=settings.mqtt_transport,
                tls=tls,
                qos=1,
            )
        except Exception as e:
            error.append(e)

    thread = threading.Thread(target=_publish, daemon=True)
    thread.start()
    thread.join(timeout=PUBLISH_TIMEOUT_SECONDS)

    if thread.is_alive():
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="MQTT broker did not respond in time",
        )
    if error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Could not reach MQTT broker: {error[0]}",
        )


@router.post("/trigger")
def trigger_door(_: str = Depends(require_auth)):
    """Sends a trigger command to the ESP32, which runs the motor for a set duration."""
    publish_command("trigger")
    return {"status": "command sent"}
