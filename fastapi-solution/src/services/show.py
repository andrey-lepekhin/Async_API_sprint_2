from functools import lru_cache

from core.config import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import Q, Search
from elasticsearch_dsl.query import MultiMatch
from fastapi import Depends
from models.filters import PaginationFilter, QueryFilter
from models.show import Show, ShowGenreFilter, ShowSortFilter
from services.utils import paginate_es_query, catch_es_not_found
from services.base import BaseService


class ShowService(BaseService):
    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic)
        self.single_item_model = Show
        self.index_name = settings.service_index_map['show']


    @catch_es_not_found
    async def get_many_with_query_filter_sort_pagination(
            self,
            query: QueryFilter = Depends(),
            filter_genre: ShowGenreFilter = Depends(),
            sort: ShowSortFilter = Depends(),
            pagination: PaginationFilter = Depends(),
    ) -> list[Show] | None:
        es_query = Search()
        if filter_genre.genre_id:
            es_query = es_query.filter(
                'nested',
                path='genres',
                query=Q('term', genres__id=filter_genre.genre_id)
            )
        if query.query:
            es_query = es_query.query(MultiMatch(
                query=query.query,
                fields=[  # Changes here will break search tests
                    'title^10',
                    'description^4',
                    'actors_names^3',
                    'director^2',
                    'writers_names^1',
                ],
                fuzziness=settings.search_fuzziness
            )
            )
        query_body = paginate_es_query(
            query=es_query,
            page_size=pagination.page_size,
            page_number=pagination.page_number
        ).to_dict()
        search = await self.elastic.search(
            index=settings.show_index_name,
            body=query_body,
            sort=sort._get_sort_for_elastic()
        )
        items = [Show(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_show_service(
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> ShowService:
    return ShowService(elastic)
