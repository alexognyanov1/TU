from fastapi import APIRouter, Depends, HTTPException, status

from auth import require_auth
from ws_manager import manager

router = APIRouter(prefix="/door", tags=["door"])


@router.post("/trigger")
async def trigger_door(_: str = Depends(require_auth)):
    """Sends a trigger command to the ESP32, which runs the motor for a set duration."""
    if not manager.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ESP32 is not connected",
        )
    if manager.get_motor_state() == "moving":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Motor is already running",
        )
    ok = await manager.send_command({"action": "trigger"})
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ESP32 is not connected",
        )
    return {"status": "command sent"}
