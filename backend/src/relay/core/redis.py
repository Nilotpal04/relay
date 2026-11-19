from redis.asyncio import Redis
from relay.core.config import get_settings

def create_redis_client() -> Redis:
    settings = get_settings()
    client = Redis.from_url(
        settings.redis_url,
        decode_responses=True
    )
    return client
