from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, Response, status
from fastapi.encoders import jsonable_encoder

from src.auth import jwt, service, utils
from src.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
    validate_swagger_auth_form,
)
from src.auth.jwt import (
    parse_jwt_user_data,
    validate_admin_access,
)
from src.auth.schemas import (
    AccessTokenResponse,
    AuthUser,
    JWTData,
    UpdateUser,
    UserResponse,
)

router = APIRouter()


@router.post(
    "/users",
    response_model_exclude_none=True,
    response_model=UserResponse,
    response_model_exclude={"id"},
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    auth_data: Annotated[AuthUser, Depends(valid_user_create)],
) -> dict[str, str]:
    user = await service.create_user(auth_data)
    return jsonable_encoder(user)


@router.get("/users/me", response_model_exclude_none=True, response_model=UserResponse)
async def my_account(
    jwt_data: Annotated[JWTData, Depends(parse_jwt_user_data)],
) -> dict[str, str]:
    user = await service.get_user_by_id(jwt_data.user_id)
    return jsonable_encoder(user)


@router.get("/users/tokeninfo", response_model=JWTData)
async def token_info(
    jwt_data: Annotated[JWTData, Depends(parse_jwt_user_data)],
) -> JWTData:
    return jwt_data


@router.patch(
    "/{user_id}/update",
    response_model=UserResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(validate_admin_access)],
)
async def update_user(
    user_id: Annotated[
        int,
        Path(
            title="ID of the item to update",
            ge=0,
        ),
    ],
    upd_data: Annotated[
        UpdateUser,
        Body(
            openapi_examples={
                "role": {
                    "summary": "Update user role",
                    "value": {
                        "is_admin": True,
                    },
                },
                "password": {
                    "summary": "Update user password",
                    "value": {
                        "password": "Pa$$w0rd!",
                    },
                },
                "email": {
                    "summary": "Update user email",
                    "value": {
                        "email": "Foo@bar.com",
                    },
                },
                "combine": {
                    "summary": "Update user email password and role",
                    "value": {
                        "email": "Foo@bar.com",
                        "is_admin": True,
                        "password": "Pa$$w0rd!",
                    },
                },
            },
        ),
    ],
) -> dict[str, str]:
    user = await service.update_user(user_id, upd_data)
    return jsonable_encoder(user)


@router.get(
    "/users/get",
    dependencies=[Depends(validate_admin_access)],
    response_model_exclude_none=True,
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def all_users() -> list[UserResponse]:
    return [UserResponse(**user) for user in await service.all_users()]


@router.delete(
    "/{user_id}/delete",
    dependencies=[Depends(validate_admin_access)],
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: Annotated[
        int,
        Path(
            title="ID of the item to delete",
            ge=0,
        ),
    ],
) -> None:
    await service.delete_user(user_id)


@router.post(
    "/users/signin", response_model=AccessTokenResponse, include_in_schema=False
)
async def auth_swagger(
    response: Response,
    auth_data: Annotated[AuthUser, Depends(validate_swagger_auth_form)],
) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(response: Response, auth_data: AuthUser) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: Annotated[dict[str, Any], Depends(valid_refresh_token)],
    user: Annotated[dict[str, Any], Depends(valid_refresh_token_user)],
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["uuid"])
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/users/tokens")
async def logout_user(
    response: Response,
    refresh_token: Annotated[dict[str, Any], Depends(valid_refresh_token)],
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )
