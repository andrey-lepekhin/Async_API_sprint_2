from typing import List, Optional, Union

import orjson
from models.common_models import Genre, Person
from models.filters import BaseSortFilter
from pydantic import UUID4, BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()

class Show(BaseModel):
    id: Union[UUID4, str]  # TODO: Redis.set fails if this is just UUID4, fix it?
    imdb_rating: Optional[float] = None
    genres: Optional[List[Genre]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    director: Optional[List[str]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[Person]] = None
    writers: Optional[List[Person]] = None

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps

class ShowGenreFilter(BaseModel):
    class Config:
        allow_population_by_field_name = True

    genre_id: UUID4 = Field(None, alias="filter__genre__")


class ShowSortFilter(BaseSortFilter):

    class Config:
        allowed_filter_field_names = ['imdb_rating']