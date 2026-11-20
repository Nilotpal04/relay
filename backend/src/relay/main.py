import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from relay.api.endpoints import router as endpoints_router
from relay.api.webhooks import router as webhooks_router
from relay.api.requests import router as requests_router
from relay.api.websocket import router as websocket_router

from relay.core.redis import create_redis_client
from relay.realtime.subscriber import RedisEventSubscriber
from relay.realtime.runtime import connection_manager
from relay.realtime.publisher import RedisEventPublisher

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = create_redis_client()
    app.state.redis = redis_client

    task = None

    try:
        await redis_client.ping()

        event_publisher = RedisEventPublisher(redis_client)
        app.state.event_publisher = event_publisher

        subscriber = RedisEventSubscriber(
            redis_client,
            connection_manager
        )

        task = asyncio.create_task(subscriber.listen())

        yield

    finally:
        if task is not None:
            task.cancel()

            with suppress(asyncio.CancelledError):
                await task

        await redis_client.aclose()


app = FastAPI(
    title="Relay API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(endpoints_router, prefix="/api")
app.include_router(webhooks_router, prefix="/api")
app.include_router(requests_router, prefix="/api")
app.include_router(websocket_router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
