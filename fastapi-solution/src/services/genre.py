import logging
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import GENRE_INDEX_NAME
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5

loggerb = logging.getLogger(__name__)


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def all(self, **kwargs) -> List[Optional[Genre]]:
        genres = get_genre_service(**kwargs)
        if not genres:
            genres = await self._get_genre_from_elastic(**kwargs)
            if not genres:
                return []
        return genres

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """
        Gets a single genre by its ID from ES.
        :param genre_id:
        :return:
        """
        genre = await self._get_genre_from_elastic(genre_id)
        if not genre:
            return None
        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[List[Genre]]:
        try:
            doc = await self.elastic.get(index=GENRE_INDEX_NAME, id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
