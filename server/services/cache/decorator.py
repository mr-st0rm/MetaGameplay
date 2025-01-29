import functools
from typing import Any

from pydantic import BaseModel
from server.services.cache.redis_cache import redis_cache_service


def serialize(result: Any) -> Any:
    if result is None:
        return result

    if isinstance(result, BaseModel):
        return result.model_dump()

    if isinstance(result, (list, tuple, set)):
        return [serialize(item) for item in result]

    return result


def cache_response(expire_ttl: int = 60):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = redis_cache_service.generate_key(func.__name__, **kwargs)

            cached_data = await redis_cache_service.get(cache_key)

            if cached_data is not None:
                return cached_data

            result = await func(*args, **kwargs)

            await redis_cache_service.set(cache_key, serialize(result), expire_ttl)

            return result

        return wrapper

    return decorator
