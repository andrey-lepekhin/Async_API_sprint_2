from typing import List

from models.mixins import BaseModelMixin
from pydantic import UUID4, Field


class Genre(BaseModelMixin):
    id: UUID4 = Field(alias="uuid")


class Person(BaseModelMixin):
    id: UUID4 = Field(alias="uuid")


class PersonShow(Person):
    role: List[str]
    film_ids: List[UUID4]
