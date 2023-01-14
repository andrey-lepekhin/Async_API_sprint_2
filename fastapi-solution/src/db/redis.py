from typing import Optional

from redis import asyncio as aioredis

redis: Optional[aioredis.Redis] = None

async def get_redis() -> aioredis.Redis:
    return redis
