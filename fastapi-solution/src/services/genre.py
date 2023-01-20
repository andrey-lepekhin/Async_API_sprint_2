from functools import lru_cache
from typing import List, Optional

from core.config import GENRE_INDEX_NAME
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from fastapi import Depends
from models.filters import PaginationFilter
from models.genre import Genre, GenreSortFilter
from services.utils import paginate_es_query


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """
        Gets a single genre by its ID from ES.
        :param genre_id:
        :return:
        """
        try:
            doc = await self.elastic.get(index=GENRE_INDEX_NAME, id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def get_many_with_filter_sort_pagination(
            self,
            sort: GenreSortFilter = Depends(),
            pagination: PaginationFilter = Depends(),
    ) -> Optional[List[Genre]]:
        s = Search()
        query = s
        query_body = paginate_es_query(
            query=query, page_size=pagination.page_size, page_number=pagination.page_number
        ).to_dict()
        search = await self.elastic.search(
            index=GENRE_INDEX_NAME, body=query_body, sort=sort._get_sort_for_elastic()
        )
        items = [Genre(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_genre_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> GenreService:
    return GenreService(elastic)
