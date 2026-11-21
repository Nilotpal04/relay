import asyncio
import json
import logging
from uuid import UUID

from redis.asyncio import Redis
from redis.exceptions import RedisError

from relay.realtime.manager import ConnectionManager

logger = logging.getLogger(__name__)

INITIAL_RETRY_DELAY = 1
MAX_RETRY_DELAY = 30


class RedisEventSubscriber:
    def __init__(
        self,
        redis: Redis,
        connection_manager: ConnectionManager,
    ) -> None:
        self.redis = redis
        self.connection_manager = connection_manager

    async def listen(self) -> None:
        retry_delay = INITIAL_RETRY_DELAY

        while True:
            try:
                await self._listen_once()
                retry_delay = INITIAL_RETRY_DELAY

            except RedisError:
                logger.exception(
                    "Redis subscriber connection failed. Retrying in %s seconds",
                    retry_delay,
                )

                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)

    async def _listen_once(self) -> None:
        pubsub = self.redis.pubsub()

        try:
            await pubsub.psubscribe("relay:endpoint:*")
            logger.info("Redis subscriber connected and listening for events")

            async for message in pubsub.listen():
                if message["type"] != "pmessage":
                    continue

                try:
                    channel = message["channel"]
                    endpoint_id = UUID(
                        channel.removeprefix("relay:endpoint:")
                    )
                    event = json.loads(message["data"])

                    await self.connection_manager.broadcast(
                        endpoint_id, event
                    )

                except Exception:
                    logger.exception(
                        "Failed to process Redis Pub/Sub message"
                    )

        finally:
            await pubsub.aclose()
