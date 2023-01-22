from typing import Union

from pydantic import UUID4

from models.filters import BaseSortFilter
from models.mixins import BaseModelMixin


class Genre(BaseModelMixin):
    id: Union[UUID4, str]
    name: str | None = None
    description: str | None = None


class GenreSortFilter(BaseSortFilter):

    class Config:
        allowed_filter_field_names = ['name', ]
