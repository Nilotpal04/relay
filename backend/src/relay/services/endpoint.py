import secrets
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from relay.models.endpoint import Endpoint
from relay.schemas.endpoint import EndpointCreate

async def create_endpoint(
        session: AsyncSession,
        payload: EndpointCreate,
) -> Endpoint:
    endpoint = Endpoint(
        name = payload.name.strip(),
        token = secrets.token_urlsafe(32),
    )

    session.add(endpoint)
    await session.commit()
    await session.refresh(endpoint)

    return endpoint

async def list_endpoints(session: AsyncSession) -> list[Endpoint]:
    result = await session.execute(
        select(Endpoint).order_by(Endpoint.created_at.desc())
    )
    return list(result.scalars().all())

async def get_endpoint(
        session: AsyncSession,
        endpoint_id: UUID,
) -> Endpoint | None:
    result = await session.execute(
        select(Endpoint).where(Endpoint.id == endpoint_id)
    )
    return result.scalar_one_or_none()

async def delete_endpoint(
        session: AsyncSession,
        endpoint: Endpoint,
) -> None:
    await session.delete(endpoint)
    await session.commit()
