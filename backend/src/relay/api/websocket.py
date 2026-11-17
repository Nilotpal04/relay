from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from relay.realtime.runtime import connection_manager

from sqlalchemy.ext.asyncio import AsyncSession
from relay.db.session import get_db_session
from relay.services.endpoint import get_endpoint_by_id

router = APIRouter(prefix="/ws", tags=["websocket"])

@router.websocket("/endpoints/{endpoint_id}")
async def endpoint_websocket(
    websocket: WebSocket,
    endpoint_id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    endpoint = await get_endpoint_by_id(session, endpoint_id)

    if endpoint is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await connection_manager.connect(websocket, endpoint_id)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, endpoint_id)
