from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from core.config import SHOW_INDEX_NAME
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Q, Search
from fastapi import Depends
from models.show import Show, ShowGenreFilter, ShowSortFilter


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

    async def get_many_with_filter_sort_pagination(
            self,
            filter_genre: ShowGenreFilter = Depends(),
            sort: ShowSortFilter = Depends(),
    ) -> Optional[List[Show]]:
        # TODO: pagination
        s = Search(using=self.elastic, index=SHOW_INDEX_NAME)
        if filter_genre:
            query = s.filter('terms', genre=['Fantasy'])[:10].to_dict()  # TODO: change to genre id from filter after changing the ES index to include it
            search = await self.elastic.search(index=SHOW_INDEX_NAME, body=query, sort=sort._get_sort_for_elastic())
            items = [Show(**hit['_source']) for hit in search['hits']['hits']]
            return items
        doc = await self.elastic.search(index=SHOW_INDEX_NAME, body={}, sort=sort._get_sort_for_elastic())
        # print(doc)
        return str(doc['hits'])
        # result = await self._get_show_list_from_elastic(filter, sort)
        # return result

    async def _get_show_list_from_elastic(self, filter=None, sort=None) -> List[Optional[Show]]:
        # doc = await self.elastic.get(index=SHOW_INDEX_NAME, id=show_id).sort("imdb_rating", {'order': "desc"}
        doc = await self.elastic.search(index=SHOW_INDEX_NAME, query={"match_all": {}})
        print(doc)
        return []


@lru_cache()
def get_show_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> ShowService:
    return ShowService(elastic)