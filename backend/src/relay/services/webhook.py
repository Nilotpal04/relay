from sqlalchemy.ext.asyncio import AsyncSession
from relay.models.webhook_request import WebhookRequest
import uuid

async def create_webhook_request(
        session: AsyncSession,
        endpoint_id: uuid.UUID,
        method: str,
        headers: dict,
        query_params: dict,
        body: bytes,
        content_type: str | None,
        source_ip: str | None,
) -> WebhookRequest:

    webhook_req = WebhookRequest(
        endpoint_id = endpoint_id,
        method = method,
        headers = headers,
        query_params = query_params,
        body=body,
        content_type = content_type,
        source_ip = source_ip,
    )

    session.add(webhook_req)

    await session.commit()
    await session.refresh(webhook_req)
    return webhook_req
