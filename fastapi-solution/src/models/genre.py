from datetime import datetime
from typing import Optional, Union

import orjson
from pydantic import UUID4, BaseModel

from models.filters import BaseSortFilter


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    id: Union[UUID4, str]  # TODO: Redis.set fails if this is just UUID4, fix it?
    name: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class GenreSortFilter(BaseSortFilter):

    class Config:
        allowed_filter_field_names = ['name']
