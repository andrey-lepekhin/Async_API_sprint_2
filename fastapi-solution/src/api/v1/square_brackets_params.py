"""Custom request router that converts square brackets in param keys.
Based on https://stackoverflow.com/a/70230211/196171"""

import re

from fastapi import Request
from fastapi.routing import APIRoute
from starlette.datastructures import QueryParams

SQUARE_BRACKETS_BECOME = '__'


def parse_param_name(param):
    regex = r"(?P<op>.*)\[(?P<col>.*)\]"
    if m := re.search(regex, param):
        return f'{m.group("op")}{SQUARE_BRACKETS_BECOME}{m.group("col")}{SQUARE_BRACKETS_BECOME}'
    return param


class BracketRequest(Request):
    @property
    def query_params(self):
        return QueryParams({parse_param_name(k): v for k, v in super().query_params.items()})


class BracketRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            request = BracketRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
