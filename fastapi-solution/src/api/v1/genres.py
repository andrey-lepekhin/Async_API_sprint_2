from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from pydantic import BaseModel, UUID4

from src.models.mixins import UUIDMixin
from src.services.genre import GenreService, get_genre_service
from services.show import ShowService, get_show_service
from models.genre import Genre

from core.config import SHOW_CACHE_EXPIRE_IN_SECONDS

router = APIRouter()


class GenreAPI(UUIDMixin, BaseModel):
    name: str


class ListGenreAPI(UUIDMixin, BaseModel):
    genres: Optional[List[Genre]] = None


class SingleGenreAPIResponse(Genre):
    pass  # Assuming no internal information in Show model, so we don't need to cut anything out


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


@router.get('/{genre_id}', response_model=SingleGenreAPIResponse)
@cache(expire=SHOW_CACHE_EXPIRE_IN_SECONDS)
async def show_details(
        show_id: str,
        show_service: ShowService = Depends(get_show_service),
) -> SingleGenreAPIResponse:
    """
    Gets a single show by its ID.
    :param show_id:
    :param show_service:
    :return:
    """
    show = await show_service.get_by_id(show_id)
    if not show:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='show not found')
    return SingleGenreAPIResponse(**show.dict())


@router.get('', response_model=ListGenreAPI)
@cache(expire=SHOW_CACHE_EXPIRE_IN_SECONDS)
async def show_list(
        query: str = None,
        show_service: ShowService = Depends(get_show_service),
) -> ListGenreAPI:
    # TODO: Implement filters and sorting
    return ListGenreAPI()