from uuid import UUID

from typing import cast
from sqlalchemy import select, delete, CursorResult
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

async def delete_webhook_request(
        session: AsyncSession,
        request_id: UUID,
) -> bool | None:
    request = await get_webhook_request(session, request_id)

    if request is None:
        return None

    await session.delete(request)
    await session.commit()

    return True

async def clear_endpoint_requests(
        session: AsyncSession,
        endpoint_id: UUID,
) -> int:
    result = await session.execute(
        delete(WebhookRequest).where(WebhookRequest.endpoint_id == endpoint_id)
    )

    await session.commit()

    cursor_result = cast(CursorResult, result)
    return cursor_result.rowcount or 0
