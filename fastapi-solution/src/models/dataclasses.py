from typing import Optional, List

from pydantic import UUID4, Field

from base import BaseModel


class BaseFilm(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float


class Genre(BaseModel):
    id: UUID4
    name: str


class PersonBase(BaseModel):
    id: UUID4 = Field(alias="uuid")
    name: str = Field(alias="full_name")


class FullFilm(BaseFilm):
    description: Optional[str] = None
    genre: List[Genre]
    actors: List[PersonBase]
    writers: Optional[List[PersonBase]] = Field(default_factory=list)
    directors: Optional[List[PersonBase]] = Field(default_factory=list)


class Person(PersonBase):
    role: List[str]
    film_ids: List[UUID4]
