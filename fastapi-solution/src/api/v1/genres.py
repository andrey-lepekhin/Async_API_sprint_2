from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from src.models.mixins import UUIDMixin
from src.services.genre import GenreService, get_genre_service

router = APIRouter()


class GenreAPI(UUIDMixin, BaseModel):
    name: str


# Pydantic supports the creation of generic models to make it easier to reuse a common model structure
@router.get('/', response_model=List[GenreAPI])
async def genre_list(
    page_size: int = Query(10, description='Number of genres on page'),
    page: int = Query(1, description='Page number'),
    sort: str = Query(
        '', description='Sorting fields (A comma-separated list pairs. '
                        'Example: name:desc)'
    ),
    genre: str = Query(None, description='Filter by genre uuid'),
    genre_service: GenreService = Depends(get_genre_service)
) -> List[GenreAPI]:
    """Returns list of genres. Each element is a dict of the GenreAPI structure."""
    genres = await genre_service.all(page_size=page_size, page=page, sort=sort, genre=genre)
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in genres]


@router.get('/search', response_model=List[GenreAPI])
async def genre_search(
    page_size: int = Query(10, description='Number of genres on page'),
    page: int = Query(1, description='Page number'),
    sort: str = Query(
        '', description='Sorting fields '
                        '(A comma-separated list of pairs. Example: name:desc)'
    ),
    query: str = Query(None, description='Part of the name (Example: comed )'),
    genre_service: GenreService = Depends(get_genre_service)
) -> List[GenreAPI]:
    """
    Returns list of genres. Each element of the list is a dict of the GenreAPI structure.
    Parameter **query**: part of genre's name.
    """
    genres = await genre_service.all(page_size=page_size, page=page, sort=sort, query=query)
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in genres]
