from typing import Union

import orjson
from models.filters import BaseSortFilter
from pydantic import UUID4, BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    id: Union[UUID4, str]
    name: str | None = None
    description: str | None = None

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class GenreSortFilter(BaseSortFilter):

    class Config:
        allowed_filter_field_names = ['name', ]
