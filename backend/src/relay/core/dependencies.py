from fastapi import Request
from redis.asyncio import Redis
from relay.realtime.publisher import RedisEventPublisher

def get_redis(request: Request) -> Redis:
    return request.app.state.redis

def get_event_publisher(request: Request) -> RedisEventPublisher:
    return request.app.state.event_publisher
