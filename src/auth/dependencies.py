from datetime import datetime
from typing import Annotated, Any

from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from src.auth import service
from src.auth.exceptions import (
    EmailTaken,
    FormValidationError,
    RefreshTokenNotFound,
    RefreshTokenNotValid,
)
from src.auth.schemas import AuthUser


async def valid_user_create(user: AuthUser) -> AuthUser:
    if await service.get_user_by_email(user.email):
        raise EmailTaken()

    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken", include_in_schema=False),
) -> dict[str, Any]:
    db_refresh_token = await service.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotFound()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> dict[str, Any]:
    user = await service.get_user_by_id(refresh_token["user_id"])
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.now() <= db_refresh_token["expires_at"]


async def validate_swagger_auth_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthUser:
    try:
        return AuthUser(email=form_data.username, password=form_data.password)
    except ValidationError as er:
        error = er.errors()[0]
        msg = error.get("msg")
        raise FormValidationError(msg)
