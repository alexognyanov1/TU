"""Door state endpoint."""

from fastapi import APIRouter, Depends

from auth import require_auth
from ws_manager import manager

router = APIRouter(prefix="/door", tags=["door"])


@router.get("/state")
def door_state_endpoint(_: str = Depends(require_auth)):
    """Returns the last known door and motor state, and whether the ESP32 is connected."""
    return {
        "door": manager.get_door_state(),
        "motor": manager.get_motor_state(),
        "esp_connected": manager.is_connected(),
    }
