from http import HTTPStatus
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from pydantic import BaseModel, UUID4

from models.filters import PaginationFilter
from services.person import PersonService, get_person_service
from models.person import Person, PersonSortFilter

from core.config import CACHE_EXPIRE_IN_SECONDS

router = APIRouter()


class SinglePersonAPIResponse(BaseModel):
    id: Union[UUID4, str]
    full_name: Optional[str] = None


# Pydantic supports the creation of generic models to make it easier to reuse a common model structure
@router.get('', response_model=Optional[List[Person]])
@cache(expire=CACHE_EXPIRE_IN_SECONDS)
async def person_list(
        person_sort_filter: PersonSortFilter = Depends(),
        pagination_filter: PaginationFilter = Depends(),
        person_service: PersonService = Depends(get_person_service),
) -> Optional[List[Person]]:
    """
    Gets a list of persons.
    :param person_service: service
    :param person_sort_filter: person filter
    :param pagination_filter: pagination filter
    :return: Optional[List[Person]]
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
