from fastapi import Request, APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from relay.db.session import get_db_session
from relay.services.endpoint import get_endpoint_by_token
from relay.services.webhook import  create_webhook_request


router = APIRouter(prefix="/hooks", tags=["Webhooks"])

@router.post("/{token}")
async def receive_webhook(
    token: str,
    request: Request,
    session: AsyncSession = Depends(get_db_session)
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

    await create_webhook_request(
        session=session,
        endpoint_id=endpoint.id,
        method=method,
        headers=headers,
        query_params=query_params,
        body=body,
        content_type=content_type,
        source_ip=source_ip,
    )

    return {"status": "accepted"}
