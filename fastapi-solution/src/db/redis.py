from abc import ABC, abstractmethod

from redis import asyncio as aioredis

redis: aioredis.Redis | None = None


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get_redis(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set_redis(self, key: str, value: str, expire: int, **kwargs):
        pass


class RedisStorage(AsyncCacheStorage):
    async def get_redis(self) -> aioredis.Redis:
        return redis

    async def set_redis(self, key: str, value: str, expire: int, **kwargs):
        pass
