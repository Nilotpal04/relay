import json
from uuid import UUID

from redis.asyncio import Redis
from relay.realtime.manager import ConnectionManager

class RedisEventSubscriber:
    def __init__(self, redis: Redis, connection_manager: ConnectionManager) -> None:
        self.redis = redis
        self.connection_manager = connection_manager

    async def listen(self) -> None:
        pubsub = self.redis.pubsub()
        await pubsub.psubscribe("relay:endpoint:*")

        try:
            async for message in pubsub.listen():
                if message["type"] != "pmessage":
                    continue

                channel = message["channel"]
                endpoint_id = UUID(channel.removeprefix("relay:endpoint:"))
                message = json.loads(message["data"])

                await self.connection_manager.broadcast(endpoint_id, message)
        finally:
            await pubsub.aclose()
