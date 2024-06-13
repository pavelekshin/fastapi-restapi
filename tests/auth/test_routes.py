import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from tests.conftest import idtype


@pytest.mark.parametrize(
    "params",
    [
        {
            "email": "fake@email.com",
            "password": "P@$$w0rd123!",
        }
    ],
    ids=idtype,
)
async def test_rates(client: TestClient, params) -> None:
    resp = await client.post("/auth/users", json=params)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json.get("email") == "fake@email.com"
