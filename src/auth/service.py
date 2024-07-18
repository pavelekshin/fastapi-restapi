import uuid
from datetime import datetime, timedelta
from typing import Any

from src.auth.config import auth_config
from src.auth.exceptions import (
    InvalidCredentialsError,
    InvalidEmailError,
    InvalidUserIDError,
)
from src.auth.schemas import AuthUser, UpdateUser
from src.auth.security import check_password, hash_password
from src.auth.utils import get_token
from src.database import auth_user, execute, fetch_all, fetch_one, refresh_tokens


async def create_user(user: AuthUser) -> dict[str, Any] | None:
    insert_query = (
        auth_user.insert()
        .values(
            {
                "email": user.email,
                "password": hash_password(user.password),
                "created_at": datetime.now(),
            }
        )
        .returning(auth_user)
    )
    return await fetch_one(insert_query)


async def update_user(user_id: int, user_data: UpdateUser) -> dict[str, Any] | None:
    user = await get_user_by_id(user_id)
    if not user:
        raise InvalidUserIDError()

    data = {
        "updated_at": datetime.now(),
    }

    if user_data.email:
        data.update(
            {
                "email": user_data.email,
            }
        )
    if user_data.password:
        data.update(
            {
                "password": hash_password(user_data.password),
            }
        )
    if user_data.is_admin is not None:
        data.update(
            {
                "is_admin": user_data.is_admin,
            }
        )

    update_query = (
        auth_user.update()
        .values(**data)
        .where(auth_user.c.id == user_id)
        .returning(auth_user)
    )

    return await fetch_one(update_query)


async def all_users():
    return await fetch_all(auth_user.select())


async def delete_user(user_id: int) -> None:
    user = await get_user_by_id(user_id)
    if not user:
        raise InvalidEmailError()

    delete_query = auth_user.delete().where(auth_user.c.id == user_id)

    await execute(delete_query)


async def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    select_query = auth_user.select().where(auth_user.c.id == user_id)

    return await fetch_one(select_query)


async def get_user_by_email(email: str) -> dict[str, Any] | None:
    select_query = auth_user.select().where(auth_user.c.email == email)

    return await fetch_one(select_query)


async def create_refresh_token(
    *, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = get_token()

    insert_query = refresh_tokens.insert().values(
        uuid=uuid.uuid4(),
        refresh_token=refresh_token,
        expires_at=datetime.now() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    await execute(insert_query)

    return refresh_token


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    select_query = refresh_tokens.select().where(
        refresh_tokens.c.refresh_token == refresh_token
    )

    return await fetch_one(select_query)


async def expire_refresh_token(refresh_token_uuid: str) -> None:
    update_query = (
        refresh_tokens.update()
        .values(expires_at=datetime.now() - timedelta(days=1))
        .where(refresh_tokens.c.uuid == refresh_token_uuid)
    )

    await execute(update_query)


async def authenticate_user(auth_data: AuthUser) -> dict[str, Any]:
    user = await get_user_by_email(auth_data.email)
    if not user:
        raise InvalidCredentialsError()

    if not check_password(auth_data.password, user["password"]):
        raise InvalidCredentialsError()

    return user
