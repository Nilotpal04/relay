from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from relay.db.session import get_db_session
from relay.schemas.endpoint import EndpointCreate, EndpointResponse
from relay.services.endpoint import (
    create_endpoint,
    list_endpoints,
    get_endpoint_by_id,
    delete_endpoint,
)

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


@router.get("", response_model=list[EndpointResponse])
async def list_endpoints_route(
    session: AsyncSession = Depends(get_db_session),
):
    return await list_endpoints(session)


@router.get("/{endpoint_id}", response_model=EndpointResponse)
async def get_endpoint_route(
    endpoint_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    endpoint = await get_endpoint_by_id(session, endpoint_id)

    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )

    return endpoint


@router.delete(
    "/{endpoint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_endpoint_route(
    endpoint_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    endpoint = await get_endpoint_by_id(session, endpoint_id)

    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )

    await delete_endpoint(session, endpoint)
