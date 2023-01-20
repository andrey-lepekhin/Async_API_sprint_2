from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field, validator


class BaseSortFilter(BaseModel):
    sort: Optional[str]

    def _get_sort_for_elastic(self):
        # TODO: add support for list of sort fields
        sort = []
        # - descending, + ascending
        if self.sort:
            if self.sort[:1] == '-':
                sort.append(f'{self.sort[1:]}:desc')
            elif self.sort[:1] == '+':
                sort.append(f'{self.sort[1:]}:asc')
            else:
                sort.append(f'{self.sort}:asc')
        return sort

    class Config:
        allowed_filter_field_names = []

    @validator("sort") # TODO: add duplicate params error
    def restrict_sortable_fields(cls, value):
        if value is None:
            return None

        allowed_field_names = cls.Config.allowed_filter_field_names

        field_name = value.replace("+", "").replace("-", "")
        if field_name not in allowed_field_names:
            raise HTTPException(HTTPStatus.BAD_REQUEST, f"You tried to sort by '{field_name}', but you may only sort by: {', '.join(allowed_field_names)}")

        return value

class PaginationFilter():
    MAX_RESULTS = 10000
    # TODO: переделать пагинацию чтобы работала на больших объемах данных, возможно с search_after эластика и прочие point in time https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html
    def __init__(
            self,
            page_size: int = Query(10, alias="page[size]", ge=1, le=1000),
            page_number: int = Query(1, alias="page[number]", ge=1),
    ):
        if page_size * page_number > self.MAX_RESULTS:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                f'Currently allowing pagination only up to {self.MAX_RESULTS} results. You\'re asking for {page_size * page_number}',
            )
        self.page_size = page_size
        self.page_number = page_number
