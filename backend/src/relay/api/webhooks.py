import logging

logger = logging.getLogger(__name__)

from fastapi import Request, APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from relay.db.session import get_db_session
from relay.services.endpoint import get_endpoint_by_token
from relay.services.webhook import  create_webhook_request

from relay.core.dependencies import get_event_publisher
from relay.realtime.publisher import EventPublisher

router = APIRouter(prefix="/hooks", tags=["Webhooks"])

@router.post("/{token}")
async def receive_webhook(
    token: str,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    event_publisher: EventPublisher = Depends(get_event_publisher)
):
    endpoint = await get_endpoint_by_token(session, token)

    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid webhook token"
        )

    body = await request.body()
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    method = request.method
    content_type = request.headers.get("content-type")
    source_ip = request.client.host if request.client else None

    webhook_req = await create_webhook_request(
        session=session,
        endpoint_id=endpoint.id,
        method=method,
        headers=headers,
        query_params=query_params,
        body=body,
        content_type=content_type,
        source_ip=source_ip,
    )

    try:
        await event_publisher.publish(
            endpoint_id=endpoint.id,
            message={
                "event": "webhook.received",
                "data": {
                    "id": str(webhook_req.id),
                    "endpoint_id": str(webhook_req.endpoint_id),
                    "method": webhook_req.method,
                    "content_type": webhook_req.content_type,
                    "source_ip": webhook_req.source_ip,
                    "received_at": webhook_req.received_at.isoformat(),
                },
            },
        )
    except Exception:
        logger.exception(f"Failed to publish real-time event for webhook {webhook_req.id}")

    return {
        "status": "accepted",
        "request_id": str(webhook_req.id)
    }
