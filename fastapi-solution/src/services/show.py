from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.es_indexes import SHOW_INDEX_NAME
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.show import Show


class ShowService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, show_id: str) -> Optional[Show]:
        """
        Gets a single show by its ID from ES.
        :param show_id:
        :return:
        """
        show = await self._get_show_from_elastic(show_id)
        if not show:
            return None
        return show

    async def _get_show_from_elastic(self, show_id: str) -> Optional[Show]:
        try:
            doc = await self.elastic.get(index=SHOW_INDEX_NAME, id=show_id)
        except NotFoundError:
            return None
        return Show(**doc['_source'])

@lru_cache()
def get_show_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> ShowService:
    return ShowService(elastic)