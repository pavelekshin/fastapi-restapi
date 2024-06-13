import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from pytest_asyncio import is_async_test

from src.main import app


# https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(autouse=True, scope="session")
def run_migration():
    os.system("alembic upgrade head")
    yield
    os.system("alembic downgrade base")


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as client:
        yield client


def idtype(val):
    if not isinstance(val, str):
        return type(val)
