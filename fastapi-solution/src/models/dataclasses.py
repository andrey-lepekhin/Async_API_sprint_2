from typing import Optional, List

from pydantic import UUID4, Field

from base import BaseModel


class Genre(BaseModel):
    id: UUID4
    name: str


class Person(BaseModel):
    id: UUID4 = Field(alias="uuid")
    name: str = Field(alias="full_name")


class Show(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float
    description: Optional[str] = None
    genre: List[Genre]
    actors: Optional[List[Person]] = None
    writers: Optional[List[Person]] = Field(default_factory=list)
    directors: Optional[List[Person]] = Field(default_factory=list)


class PersonShow(Person):
    role: List[str]
    film_ids: List[UUID4]
