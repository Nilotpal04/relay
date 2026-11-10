import secrets

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
