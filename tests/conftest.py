"""Fixtures"""
import asyncio
from dataclasses import dataclass

import aiohttp
import pytest
from multidict import CIMultiDictProxy

from tests.functional.settings import test_settings

pytest_plugins = ("functional.fixtures.elastic", "functional.fixtures.async_http", )


def pytest_configure():
    pytest.strange_unicode_str = '\uFFFF~παΈπ’π―Ω€αΈΤΠΗπΖΤΈβ²πΰ§¦Ξ‘π€Ιπ’ΘΠ¦π±Ρ π§Ζ³Θ€Ρ§α―Δπ±α»ππαΉπ²ππΔΌαΉΕΠΎππα΅²κ±π©α»«πΕ΅ππΕΊοΏ½οΏ½οΏ½!@#$%^&*()ε€§-_=+[{]};:'


@pytest.fixture(scope="session")
def event_loop():
    """
    Redefining Pytest default function-scoped event_loop fixture.
    A hack from https://stackoverflow.com/a/72104554/196171 prevents 'RuntimeError: Event loop is closed'
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
