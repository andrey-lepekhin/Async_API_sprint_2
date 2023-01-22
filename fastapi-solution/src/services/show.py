from functools import lru_cache
from typing import List

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Q, Search
from fastapi import Depends

from core.config import SHOW_INDEX_NAME
from db.elastic import get_elastic
from models.filters import PaginationFilter, QueryFilter
from models.show import Show, ShowGenreFilter, ShowSortFilter
from services.utils import paginate_es_query


class ShowService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, show_id: str) -> Show | None:
        """
        Gets a single show by its ID from ES.
        :param show_id: id
        :return: Show | None
        """
        try:
            doc = await self.elastic.get(index=SHOW_INDEX_NAME, id=show_id)
        except NotFoundError:
            return None
        return Show(**doc['_source'])

    async def get_many_with_query_filter_sort_pagination(
            self,
            query: QueryFilter = Depends(),
            filter_genre: ShowGenreFilter = Depends(),
            sort: ShowSortFilter = Depends(),
            pagination: PaginationFilter = Depends(),
    ) -> List[Show] | None:
        s = Search()
        es_query = s
        if filter_genre.genre_id:
            es_query = s.filter(
                'nested', path='genres', query=Q('term', genres__id=filter_genre.genre_id)
            )
        if query.query:
            es_query = es_query.query(
                "multi_match",
                query=query.query,
                fields=[
                    'title^5',
                    'description^4',
                    'actors_names^3',
                    'director^2',
                    'writers_names^1',
                ]
            )
        query_body = paginate_es_query(
            query=es_query, page_size=pagination.page_size, page_number=pagination.page_number
        ).to_dict()
        search = await self.elastic.search(
            index=SHOW_INDEX_NAME, body=query_body, sort=sort._get_sort_for_elastic()
        )
        items = [Show(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_show_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> ShowService:
    return ShowService(elastic)
