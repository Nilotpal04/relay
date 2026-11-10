from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from relay.db.session import get_db_session
from relay.schemas.endpoint import EndpointCreate, EndpointResponse
from relay.services.endpoint import create_endpoint

router = APIRouter(prefix="/endpoints", tags=["Endpoints"])

@router.post(
    "",
    response_model=EndpointResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_endpoint_route(
    payload: EndpointCreate,
    session: AsyncSession = Depends(get_db_session),
) -> EndpointResponse:
    endpoint = await create_endpoint(session, payload)
    return EndpointResponse.model_validate(endpoint)

