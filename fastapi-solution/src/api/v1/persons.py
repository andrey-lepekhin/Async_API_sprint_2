from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from api.v1.square_brackets_params import BracketRoute
from models.filters import PaginationFilter
from services.person import PersonService, get_person_service
from models.person import Person, PersonSortFilter

from core.config import CACHE_EXPIRE_IN_SECONDS

router = APIRouter()
router.route_class = BracketRoute


class SinglePersonAPIResponse(Person):
    pass  # Assuming no internal information in Person model, so we don't need to cut anything out


# Pydantic supports the creation of generic models to make it easier to reuse a common model structure
@router.get('/', response_model=List[Person])
@cache(expire=CACHE_EXPIRE_IN_SECONDS)
async def person_list(
        person_sort_filter: PersonSortFilter = Depends(),
        pagination_filter: PaginationFilter = Depends(),
        person_service: PersonService = Depends(get_person_service),
) -> Optional[List[Person]]:
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
    :param person_id:
    :param person_service:
    :return:
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return SinglePersonAPIResponse(**person.dict())
