from functools import lru_cache
from typing import List, Optional

from core.config import SHOW_INDEX_NAME
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Q, Search
from fastapi import Depends
from models.filters import PaginationFilter
from models.show import Show, ShowGenreFilter, ShowSortFilter
from services.utils import paginate_es_query


class ShowService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, show_id: str) -> Optional[Show]:
        """
        Gets a single show by its ID from ES.
        :param show_id:
        :return:
        """
        try:
            doc = await self.elastic.get(index=SHOW_INDEX_NAME, id=show_id)
        except NotFoundError:
            return None
        return Show(**doc['_source'])


    async def get_many_with_filter_sort_pagination(
            self,
            filter_genre: ShowGenreFilter = Depends(),
            sort: ShowSortFilter = Depends(),
            pagination: PaginationFilter = Depends(),
    ) -> Optional[List[Show]]:
        s = Search()
        query = s
        if filter_genre.genre_id:
            query = s.filter('nested', path='genres', query=Q('term', genres__id=filter_genre.genre_id))
        query_body = paginate_es_query(query=query, page_size=pagination.page_size, page_number=pagination.page_number).to_dict()
        search = await self.elastic.search(index=SHOW_INDEX_NAME, body=query_body, sort=sort._get_sort_for_elastic())
        items = [Show(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_show_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> ShowService:
    return ShowService(elastic)