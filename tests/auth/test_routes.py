import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from src.auth.constants import ErrorCode
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
async def test_register_email_taken(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, params
) -> None:
    from src.auth.dependencies import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_email", fake_getter)

    resp = await client.post("/auth/users", json=params)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp_json["error"]["error_code"] == ErrorCode.EMAIL_TAKEN
