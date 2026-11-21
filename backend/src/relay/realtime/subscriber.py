import json
from uuid import UUID

import logging

logger = logging.getLogger(__name__)

from redis.asyncio import Redis
from relay.realtime.manager import ConnectionManager

class RedisEventSubscriber:
    def __init__(self, redis: Redis, connection_manager: ConnectionManager) -> None:
        self.redis = redis
        self.connection_manager = connection_manager

    async def listen(self) -> None:
        pubsub = self.redis.pubsub()

        try:
            await pubsub.psubscribe("relay:endpoint:*")

            async for message in pubsub.listen():
                if message["type"] != "pmessage":
                    continue

                try:
                    channel = message["channel"]
                    endpoint_id = UUID(channel.removeprefix("relay:endpoint:"))
                    event = json.loads(message["data"])

                    await self.connection_manager.broadcast(endpoint_id, event)

                except Exception:
                    logger.exception("Failed to process Redis Pub/Sub message")

        finally:
            await pubsub.aclose()
