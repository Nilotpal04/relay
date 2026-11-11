from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from relay.db.session import get_db_session
from relay.services.endpoint import get_endpoint_by_id
from relay.services.request import (
    get_webhook_request,
    list_webhook_requests,
    delete_webhook_request,
    clear_endpoint_requests,
)
from relay.schemas.webhook_request import (
    WebhookRequestSummary,
    WebhookRequestDetail,
)

router = APIRouter(prefix="/requests", tags=["Requests"])

@router.get ("/endpoints/{endpoint_id}/requests", response_model=list[WebhookRequestSummary])
async def list_requests_route(
    endpoint_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    endpoint = await get_endpoint_by_id(session, endpoint_id)
    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found"
        )

    return await list_webhook_requests(
        session=session,
        endpoint_id=endpoint_id,
        limit=limit,
        offset=offset
    )


@router.get(
    "/{request_id}",
    response_model=WebhookRequestDetail
)
async def get_request_route(
    request_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    webhook_request = await get_webhook_request(session, request_id)

    if not webhook_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook request not found"
        )

    return webhook_request

@router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_request_route(
    request_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    success = await delete_webhook_request(session, request_id)

    if success is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook request not found",
        )

    return None

@router.delete(
    "/endpoints/{endpoint_id}/requests",
    status_code=status.HTTP_200_OK,
)
async def clear_requests_route(
    endpoint_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    endpoint = await get_endpoint_by_id(session, endpoint_id)
    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )

    deleted_count = await clear_endpoint_requests(session, endpoint_id)

    return {
        "status": "success",
        "deleted_count": deleted_count
    }
