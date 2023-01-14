from http import HTTPStatus
from typing import List, Optional

from core.config import SHOW_CACHE_EXPIRE_IN_SECONDS
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from models.show import Show
from pydantic import UUID4, BaseModel
from services.show import ShowService, get_show_service

router = APIRouter()

class SingleShowAPIResponse(Show):
    pass  # Assuming no internal information in Show model, so we don't need to cut anything out

class ManyShowAPIResponse(BaseModel):
    shows: Optional[List[Show]] = None


@router.get('/{show_id}', response_model=SingleShowAPIResponse)
@cache(expire=SHOW_CACHE_EXPIRE_IN_SECONDS)
async def show_details(
        show_id: str,
        show_service: ShowService = Depends(get_show_service),
) -> SingleShowAPIResponse:
    """
    Gets a single show by its ID.
    :param show_id:
    :param show_service:
    :return:
    """
    show = await show_service.get_by_id(show_id)
    if not show:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='show not found')
    return SingleShowAPIResponse(**show.dict())


@router.get('', response_model=ManyShowAPIResponse)
@cache(expire=SHOW_CACHE_EXPIRE_IN_SECONDS)
async def show_list(
        query: str = None,
        show_service: ShowService = Depends(get_show_service),
) -> ManyShowAPIResponse:
    # TODO: Implement filters and sorting
    return ManyShowAPIResponse()