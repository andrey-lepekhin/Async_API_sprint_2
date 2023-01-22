from typing import List, Union

import orjson
from fastapi import Query
from models.common_models import Genre, Person
from models.filters import BaseSortFilter
from pydantic import UUID4, BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Show(BaseModel):
    id: Union[UUID4, str]  # TODO: Redis.set fails if this is just UUID4, fix it?
    imdb_rating: float | None = None
    genres: List[Genre | None] = None
    title: str | None = None
    description: str | None = None
    director: List[str] | None = None
    actors_names: List[str] | None = None
    writers_names: List[str] | None = None
    actors: List[Person] | None = None
    writers: List[Person] | None = None

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ShowGenreFilter:
    def __init__(
            self,
            genre_id: str = Query(
                None,
                description='Genre UUID4, which is used to output '
                            'only Shows with corresponding genres',
                alias='filter[genre]',
            ),
    ):
        self.genre_id = genre_id


class ShowSortFilter(BaseSortFilter):

    class Config:
        allowed_filter_field_names = ['imdb_rating']
