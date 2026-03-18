"""WebSocket connection managers for the ESP32 device and browser UI clients."""

from fastapi import WebSocket


class ESP32Manager:
    """Tracks the ESP32 connection, door state, and motor state.
    Broadcasts updates to all connected browser clients immediately.
    """

    def __init__(self):
        self._ws: WebSocket | None = None
        self._door_state: str = "unknown"   # open | closed | unknown
        self._motor_state: str = "idle"     # idle | moving
        self._ui_clients: list[WebSocket] = []

    # --- ESP32 connection ---

    async def set_ws(self, ws: WebSocket | None):
        self._ws = ws
        if ws is None:
            # Device disconnected — reset motor, keep last door state.
            self._motor_state = "idle"
        await self._broadcast()

    async def send_command(self, payload: dict) -> bool:
        """Sends a JSON command to the ESP32. Returns False if not connected."""
        if self._ws is None:
            return False
        try:
            await self._ws.send_json(payload)
            return True
        except Exception:
            self._ws = None
            return False

    def is_connected(self) -> bool:
        return self._ws is not None

    # --- State updates (called when ESP32 sends a message) ---

    async def update(self, door: str | None, motor: str | None):
        """Updates one or both state fields and broadcasts to all UI clients."""
        if door is not None:
            self._door_state = door
        if motor is not None:
            self._motor_state = motor
        await self._broadcast()

    def get_door_state(self) -> str:
        return self._door_state

    def get_motor_state(self) -> str:
        return self._motor_state

    # --- UI client registry ---

    async def add_ui_client(self, ws: WebSocket):
        self._ui_clients.append(ws)
        # Send current state immediately so the page renders correctly on connect.
        try:
            await ws.send_json(self._current_payload())
        except Exception:
            pass

    def remove_ui_client(self, ws: WebSocket):
        self._ui_clients = [c for c in self._ui_clients if c is not ws]

    async def _broadcast(self):
        payload = self._current_payload()
        dead = []
        for client in self._ui_clients:
            try:
                await client.send_json(payload)
            except Exception:
                dead.append(client)
        for d in dead:
            self._ui_clients.remove(d)

    def _current_payload(self) -> dict:
        return {
            "door": self._door_state,
            "motor": self._motor_state,
            "esp_connected": self._ws is not None,
        }


manager = ESP32Manager()
