from http import HTTPStatus
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from pydantic import UUID4, BaseModel

from models.filters import PaginationFilter
from services.genre import GenreService, get_genre_service
from models.genre import Genre, GenreSortFilter

from core.config import CACHE_EXPIRE_IN_SECONDS

router = APIRouter()


class SingleGenreAPIResponse(BaseModel):
    id: Union[UUID4, str]
    name: Optional[str] = None
    description: Optional[str] = None


# Pydantic supports the creation of generic models to make it easier to reuse a common model structure
@router.get('', response_model=Optional[List[Genre]])
@cache(expire=CACHE_EXPIRE_IN_SECONDS)
async def genre_list(
        genre_sort_filter: GenreSortFilter = Depends(),
        pagination_filter: PaginationFilter = Depends(),
        genre_service: GenreService = Depends(get_genre_service),
) -> Optional[List[Genre]]:
    items = await genre_service.get_many_with_filter_sort_pagination(
        sort=genre_sort_filter,
        pagination=pagination_filter,
    )
    return items


@router.get('/{genre_id}', response_model=SingleGenreAPIResponse)
@cache(expire=CACHE_EXPIRE_IN_SECONDS)
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
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'id:"{genre_id}" is not found')
    return SingleGenreAPIResponse(**genre.dict())
