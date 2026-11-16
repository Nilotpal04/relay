from uuid import UUID
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, endpoint_id: UUID):
        await websocket.accept()
        self.active_connections.setdefault(endpoint_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, endpoint_id: UUID):
        if endpoint_id in self.active_connections:
            connections = self.active_connections[endpoint_id]

            if websocket in connections:
                connections.remove(websocket)

            if not connections:
                del self.active_connections[endpoint_id]

    async def broadcast(self, endpoint_id: UUID, message: dict):
        if endpoint_id not in self.active_connections:
            return

        connections = list(self.active_connections[endpoint_id])

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except (WebSocketDisconnect, OSError):
                self.disconnect(websocket, endpoint_id)
