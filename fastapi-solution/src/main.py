import logging
import os
import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import genres
from core import config
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
    redis.redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=os.environ.get('REDIS_HOST'),
        port=os.environ.get('REDIS_PORT'),
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
    # For hiding uvicorn propagates
    logger = logging.getLogger('uvicorn.error')
    logger.propagate = False
