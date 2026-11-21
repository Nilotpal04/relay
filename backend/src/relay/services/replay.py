import time
from uuid import UUID

import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from relay.models.replay import ReplayAttempt
from relay.services.request import get_webhook_request
from relay.services.replay_security import validate_destination

MAX_RESPONSE_SIZE = 1_000_000
REQUEST_TIMEOUT = 10.0

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


async def create_replay(
    session: AsyncSession,
    request_id: UUID,
    destination_url: str,
) -> ReplayAttempt | None:

    original = await get_webhook_request(session, request_id)

    if original is None:
        return None

    validate_destination(destination_url)

    headers = {
        key: value
        for key, value in original.headers.items()
        if key.lower() not in HOP_BY_HOP_HEADERS
    }

    attempt = ReplayAttempt(
        request_id=original.id,
        destination_url=destination_url,
        method=original.method,
        request_headers=headers,
        request_body=original.body,
        status="failed",
    )

    session.add(attempt)

    start_time = time.perf_counter()

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            follow_redirects=False,
        ) as client:

            async with client.stream(
                method=original.method,
                url=destination_url,
                params=original.query_params,
                headers=headers,
                content=original.body,
            ) as response:

                response_body = bytearray()

                async for chunk in response.aiter_bytes():
                    response_body.extend(chunk)

                    if len(response_body) > MAX_RESPONSE_SIZE:
                        raise ValueError("Destination response exceeded size limit.")

                attempt.status = "completed"
                attempt.response_status_code = response.status_code
                attempt.response_headers = dict(response.headers)
                attempt.response_body = bytes(response_body)

    except Exception as exc:
        attempt.status = "failed"
        attempt.error = str(exc)[:2000]

    finally:
        attempt.duration_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

    await session.commit()
    await session.refresh(attempt)

    return attempt
