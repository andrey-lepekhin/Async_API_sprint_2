import logging
from functools import lru_cache
from typing import List, Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre
from db.es_indexes import SHOW_INDEX_NAME

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5

loggerb = logging.getLogger(__name__)


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """
        Gets a single show by its ID from ES.
        :param show_id:
        :return:
        """
        genre = await self._get_genre_from_elastic(genre_id)
        if not genre:
            return None
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[List[Genre]]:
        try:
            doc = await self.elastic.get(index=SHOW_INDEX_NAME, id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
