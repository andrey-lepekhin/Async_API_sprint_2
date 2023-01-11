from typing import Optional, List

from pydantic import UUID4, Field

from base import BaseModel


class Filmwork(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float


class Genre(BaseModel):
    id: UUID4
    name: str


class PersonFilmwork(BaseModel):
    id: UUID4 = Field(alias="uuid")
    name: str = Field(alias="full_name")


class FullFilm(Filmwork):
    description: Optional[str] = None
    genre: List[Genre]
    actors: Optional[List[PersonFilmwork]] = None
    writers: Optional[List[PersonFilmwork]] = Field(default_factory=list)
    directors: Optional[List[PersonFilmwork]] = Field(default_factory=list)


class Person(PersonFilmwork):
    role: List[str]
    film_ids: List[UUID4]
