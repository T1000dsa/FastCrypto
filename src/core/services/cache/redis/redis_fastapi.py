import pickle
import hashlib
import gzip
from typing import Optional, Any, Callable, Union
from functools import wraps
from fastapi import Request
from redis.asyncio import Redis
from datetime import timedelta

from src.core.config.settings import settings


class RedisCacheService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached data with automatic decompression"""
        cached = await self.redis.get(key)
        if cached is None:
            return None
        
        try:
            # Try to decompress first (for gzip compressed data)
            return pickle.loads(gzip.decompress(cached))
        except:
            try:
                # Fall back to regular pickle
                return pickle.loads(cached)
            except:
                # Return raw data if not pickled
                return cached.decode()

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = settings.redis.REDIS_CACHE_TTL,
        compress: bool = True
    ) -> None:
        """Set cached data with optional compression"""
        serialized = pickle.dumps(value)
        if compress:
            serialized = gzip.compress(serialized)
        await self.redis.setex(key, timedelta(hours=ttl), serialized)

    async def delete(self, key: str) -> None:
        """Delete cached data"""
        await self.redis.delete(key)

    async def get_stats(self) -> dict:
        """Get Redis cache statistics"""
        memory_info = await self.redis.info("MEMORY")
        stats = await self.redis.info("STATS")
        hits = stats["keyspace_hits"]
        misses = stats["keyspace_misses"]
        hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
        
        return {
            "memory_used": memory_info["used_memory_human"],
            "hit_rate": hit_rate,
            "hits": hits,
            "misses": misses
        }

    def cache(
        self,
        ttl: int = 300,
        key_prefix: str = "cache",
        vary_on: Optional[list[str]] = None
    ) -> Callable:
        """
        Decorator for caching endpoint responses
        
        Args:
            ttl: Time to live in seconds
            key_prefix: Prefix for cache keys
            vary_on: List of kwargs names to include in cache key
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Skip caching if Redis is not available
                if not self.redis:
                    return await func(*args, **kwargs)
                
                # Find request object in args/kwargs
                request = kwargs.get("request", None)
                if not request:
                    for arg in args:
                        if isinstance(arg, Request):
                            request = arg
                            break
                
                # Build cache key
                cache_key = f"{key_prefix}:{func.__module__}:{func.__name__}"
                
                # Include request-specific data
                if request:
                    if request.method == "GET" and request.query_params:
                        query_hash = hashlib.md5(str(request.query_params).encode()).hexdigest()
                        cache_key += f":{query_hash}"
                    else:
                        body = await request.body()
                        if body:
                            body_hash = hashlib.md5(body).hexdigest()
                            cache_key += f":{body_hash}"
                
                # Include specified kwargs in cache key
                if vary_on:
                    for param in vary_on:
                        if param in kwargs:
                            param_hash = hashlib.md5(str(kwargs[param]).encode()).hexdigest()
                            cache_key += f":{param}:{param_hash}"
                
                # Try to get cached result
                cached_result = await self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Call original function if no cache hit
                result = await func(*args, **kwargs)
                
                # Cache the result
                await self.set(cache_key, result, ttl)
                
                return result
            
            return wrapper
        return decorator


# Initialize the service
redis = Redis(
    host=settings.redis.host, 
    port=settings.redis.port,
    db=settings.redis.db,
    decode_responses=False
)

cache_service = RedisCacheService(redis)