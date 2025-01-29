import hashlib
import json
from typing import Any

from aioredis import Redis

from server.config.cfg import get_config
from server.services.cache.base import AbstractCache


class RedisCache(AbstractCache):
    cache: Redis

    def __init__(self):
        config = get_config()
        super().__init__(
            Redis.from_url(config.cache.URL, decode_responses=True),
        )

    @staticmethod
    def generate_key(func_name: str, **kwargs) -> str:
        key_str = f"{func_name}|" + "|".join(
            f"{k}:{v}" for k, v in sorted(kwargs.items())
        )
        return hashlib.md5(key_str.encode()).hexdigest()

    async def get(self, key: str) -> Any | None:
        cached_value = await self.cache.get(key)
        return json.loads(cached_value) if cached_value else None

    async def set(self, key: str, value: Any, expire: int) -> None:
        await self.cache.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str | list[str]) -> None:
        if isinstance(key, str):
            await self.cache.delete(key)
        else:
            await self.cache.delete(*key)


redis_cache_service = RedisCache()
