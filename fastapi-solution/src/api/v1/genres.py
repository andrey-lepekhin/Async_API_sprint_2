from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from pydantic import BaseModel, UUID4

from models.filters import PaginationFilter
from models.mixins import UUIDMixin
from services.genre import GenreService, get_genre_service
from models.genre import Genre, GenreSortFilter

from core.config import SHOW_CACHE_EXPIRE_IN_SECONDS

router = APIRouter()


class GenreAPI(UUIDMixin, BaseModel):
    name: str


class ListGenreAPI(UUIDMixin, BaseModel):
    genres: Optional[List[Genre]] = None


class SingleGenreAPIResponse(Genre):
    pass  # Assuming no internal information in Genre model, so we don't need to cut anything out


# Pydantic supports the creation of generic models to make it easier to reuse a common model structure
@router.get('/', response_model=List[GenreAPI])
@cache(expire=SHOW_CACHE_EXPIRE_IN_SECONDS)
async def genre_list(
        genre_sort_filter: GenreSortFilter = Depends(),
        pagination_filter: PaginationFilter = Depends(),
        genre_service: GenreService = Depends(get_genre_service),
) -> Optional[List[GenreAPI]]:
    items = await genre_service.get_many_with_filter_sort_pagination(
        sort=genre_sort_filter,
        pagination=pagination_filter,
    )
    return items


@router.get('/{genre_id}', response_model=SingleGenreAPIResponse)
@cache(expire=SHOW_CACHE_EXPIRE_IN_SECONDS)
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service),
) -> SingleGenreAPIResponse:
    """
    Gets a single genre by its ID.
    :param genre_id:
    :param genre_service:
    :return:
    """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return SingleGenreAPIResponse(**genre.dict())
