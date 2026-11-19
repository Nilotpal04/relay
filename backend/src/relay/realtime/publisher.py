from abc import ABC, abstractmethod
from uuid import UUID
from relay.realtime.manager import ConnectionManager

import json
from redis.asyncio import Redis

class EventPublisher(ABC):

    @abstractmethod
    async def publish(self, endpoint_id: UUID, message: dict):
        ...

class InMemoryEventPublisher(EventPublisher):
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    async def publish(self, endpoint_id: UUID, message: dict):
        await self.connection_manager.broadcast(endpoint_id, message)

class RedisEventPublisher(EventPublisher):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def publish(self, endpoint_id: UUID, message: dict) -> None:
        json_string = json.dumps(message)

        channel_name = f"relay:endpoint:{endpoint_id}"
        await self.redis.publish(channel_name, json_string)
