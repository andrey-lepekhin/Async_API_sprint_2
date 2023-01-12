from typing import Optional, List

from pydantic import UUID4, Field

from base import BaseModel


class Genre(BaseModel):
    id: UUID4
    name: str


class PersonShow(BaseModel):
    id: UUID4 = Field(alias="uuid")
    name: str = Field(alias="full_name")


class Show(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float
    description: Optional[str] = None
    genre: List[Genre]
    actors: Optional[List[PersonShow]] = None
    writers: Optional[List[PersonShow]] = Field(default_factory=list)
    directors: Optional[List[PersonShow]] = Field(default_factory=list)


class Person(PersonShow):
    role: List[str]
    film_ids: List[UUID4]
