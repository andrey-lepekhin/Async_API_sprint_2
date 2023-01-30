from abc import ABC, abstractmethod
from elasticsearch import AsyncElasticsearch, NotFoundError

from models.genre import Genre
from models.person import Person
from models.show import Show


class BaseService(ABC):
    index_name: str
    single_item_model: type

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(
            self,
            id: str,
    ) -> None | list[Genre] | list[Person] | list[Show]:
        #TODO: how to implement a better method return type hint here? -> self.single_item_model doesn't work
        """
        Get a single self.single_item_model type item by its id from self.index_name index in Elastic.
        :param id:
        :return:
        """
        try:
            doc = await self.elastic.get(
                index=self.index_name, id=id
            )
        except NotFoundError:
            return None
        return self.single_item_model(**doc['_source'])

    @abstractmethod
    async def get_many_with_query_filter_sort_pagination(
            self,
            query,
            filter,
            sort,
            pagination,
    ):
        pass
