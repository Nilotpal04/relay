from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from relay.models.webhook_request import WebhookRequest

async def list_webhook_requests(
        session: AsyncSession,
        endpoint_id: UUID,
        limit: int = 20,
        offset: int = 0,
) -> list[WebhookRequest]:
    result = await session.execute(
        select(WebhookRequest)
        .where(WebhookRequest.endpoint_id == endpoint_id)
        .order_by(WebhookRequest.received_at.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(result.scalars().all())

async def get_webhook_request(
        session: AsyncSession,
        request_id: UUID,
) -> WebhookRequest | None :
    result = await session.execute(
        select(WebhookRequest).where(WebhookRequest.id == request_id)
    )

    return result.scalar_one_or_none()
