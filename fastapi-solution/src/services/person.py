from functools import lru_cache

from core.config import settings
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from fastapi import Depends
from models.filters import PaginationFilter, QueryFilter
from models.person import Person, PersonSortFilter
from services.utils import paginate_es_query


class PersonService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Person | None:
        """
        Gets a single person by its ID from ES.
        :param person_id: id
        :return: Person | None
        """
        try:
            doc = await self.elastic.get(
                index=settings.person_index_name, id=person_id
            )
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def get_many_with_query_filter_sort_pagination(
            self,
            query: QueryFilter = Depends(),
            # sort: PersonSortFilter = Depends(),
            pagination: PaginationFilter = Depends(),
    ) -> list[Person] | None:
        s = Search()
        es_query = s
        if query.query:
            es_query = es_query.query(
                "multi_match",
                query=query.query,
                fields=[
                    'full_name',
                ]
            )
        query_body = paginate_es_query(
            query=es_query,
            page_size=pagination.page_size,
            page_number=pagination.page_number
        ).to_dict()
        search = await self.elastic.search(
            index=settings.person_index_name,
            body=query_body,
            # sort=sort._get_sort_for_elastic() # TODO: add support for this in index or remove sort
        )
        items = [Person(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(elastic)
