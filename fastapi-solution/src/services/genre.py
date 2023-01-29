from functools import lru_cache

from core.config import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from fastapi import Depends
from models.filters import PaginationFilter
from models.genre import Genre, GenreSortFilter
from services.utils import paginate_es_query
from services.base import BaseService


class GenreService(BaseService):
    def __init__(self, elastic: AsyncElasticsearch):
        super().__init__(elastic)
        self.single_item_model = Genre
        self.index_name = settings.service_index_map['genre']


    async def get_many_with_query_filter_sort_pagination(
            self,
            query=None,
            sort=None,
            filter=None,
            pagination: PaginationFilter = Depends(),
    ) -> list[Genre] | None:
        s = Search()
        es_query = s
        if query.query:
            es_query = es_query.query(
                MultiMatch(
                    query=query.query,
                    fields=["name^2", "description^1"],
                    fuzziness=settings.search_fuzziness
                )
            )
        query_body = paginate_es_query(
            query=es_query,
            page_size=pagination.page_size,
            page_number=pagination.page_number
        ).to_dict()
        search = await self.elastic.search(
            index=settings.genre_index_name,
            body=query_body,
        )
        items = [Genre(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(elastic)
