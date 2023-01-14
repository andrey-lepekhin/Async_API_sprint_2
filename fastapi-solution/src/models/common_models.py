from typing import List, Optional

from models.base import BaseModel
from pydantic import UUID4, Field


class Genre(BaseModel):
    id: UUID4
    name: str


class Person(BaseModel):
    id: UUID4 = Field(alias="uuid")
    name: str = Field(alias="full_name")


class PersonShow(Person):
    role: List[str]
    film_ids: List[UUID4]
