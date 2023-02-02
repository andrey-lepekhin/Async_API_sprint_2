from redis import asyncio as aioredis

from db.base import AsyncCacheStorage

redis: aioredis.Redis | None = None


async def get_aioredis() -> aioredis.Redis:
    return redis


class RedisStorage(AsyncCacheStorage):

    async def get(self) -> aioredis.Redis:
        return redis

    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass