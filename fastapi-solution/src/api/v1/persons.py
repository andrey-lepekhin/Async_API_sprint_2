from http import HTTPStatus
from typing import List, Union

from core.config import CACHE_EXPIRE_IN_SECONDS
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from models.filters import PaginationFilter
from models.person import Person, PersonSortFilter
from pydantic import UUID4, BaseModel
from services.person import PersonService, get_person_service

router = APIRouter()


class SinglePersonAPIResponse(BaseModel):
    id: Union[UUID4, str]
    full_name: str | None = None


# Pydantic supports the creation of generic models to make it easier to reuse a common model structure
@router.get('', response_model=List[Person] | None)
@cache(expire=CACHE_EXPIRE_IN_SECONDS)
async def person_list(
        person_sort_filter: PersonSortFilter = Depends(),
        pagination_filter: PaginationFilter = Depends(),
        person_service: PersonService = Depends(get_person_service),
) -> List[Person] | None:
    """
    Gets a list of persons.
    :param person_service: service
    :param person_sort_filter: person filter
    :param pagination_filter: pagination filter
    :return: List[Person] | None
    """
    items = await person_service.get_many_with_filter_sort_pagination(
        sort=person_sort_filter,
        pagination=pagination_filter,
    )
    return items


@router.get('/{person_id}', response_model=SinglePersonAPIResponse)
@cache(expire=CACHE_EXPIRE_IN_SECONDS)
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service),
) -> SinglePersonAPIResponse:
    """
    Gets a single person by its ID.
    :param person_id: id
    :param person_service: service
    :return: SinglePersonAPIResponse
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"id: '{person_id}' is not found")
    return SinglePersonAPIResponse(**person.dict())
