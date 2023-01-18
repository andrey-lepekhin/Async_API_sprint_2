from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator


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