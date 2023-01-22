import logging
import os

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from api.v1.api import api_router as api_router_v1
from core import config
from core.config import API_V1_BASE_ROUTE
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    elastic.es = AsyncElasticsearch(
        hosts=[f'http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}']
    )
    redis.redis = aioredis.from_url(
        f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}',
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis.redis), prefix="fastapi-cache")


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(api_router_v1, prefix=API_V1_BASE_ROUTE)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=os.environ.get('SERVER_HOST'),
        port=int(os.environ.get('SERVER_PORT')),
        log_config=config.LOGGING,
        log_level=config.LOG_LEVEL,
    )
