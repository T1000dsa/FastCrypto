from redis.asyncio import Redis

from src.core.config.settings import settings


redis = Redis(
    host=settings.redis.host, 
    port=settings.redis.port,
    db=settings.redis.db
)