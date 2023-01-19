from functools import lru_cache
from typing import List, Optional

from core.config import PERSON_INDEX_NAME
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Q, Search
from fastapi import Depends
from models.filters import PaginationFilter
from models.person import Person, PersonSortFilter
from services.utils import paginate_es_query


class PersonService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        """
        Gets a single person by its ID from ES.
        :param person_id:
        :return:
        """
        try:
            doc = await self.elastic.get(index=PERSON_INDEX_NAME, id=person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def get_many_with_filter_sort_pagination(
            self,
            sort: PersonSortFilter = Depends(),
            pagination: PaginationFilter = Depends(),
    ) -> Optional[List[Person]]:
        s = Search()
        query = s
        query_body = paginate_es_query(query=query, page_size=pagination.page_size, page_number=pagination.page_number).to_dict()
        search = await self.elastic.search(index=PERSON_INDEX_NAME, body=query_body, sort=sort._get_sort_for_elastic())
        items = [Person(**hit['_source']) for hit in search['hits']['hits']]
        return items


@lru_cache()
def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> PersonService:
    return PersonService(elastic)