from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from relay.realtime.manager import ConnectionManager

router = APIRouter(prefix="/ws", tags=["websocket"])

manager = ConnectionManager()

@router.websocket("/endpoints/{endpoint_id}")
async def endpoint_websocket(websocket: WebSocket, endpoint_id: UUID):
    await manager.connect(websocket, endpoint_id)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket, endpoint_id)
