import datetime
import re
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import (
    AfterValidator,
    EmailStr,
    Field,
    PlainSerializer,
    ValidationInfo,
)

from src.models.models import CustomModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


def valid_password(password: str, info: ValidationInfo) -> str:
    if not re.match(STRONG_PASSWORD_PATTERN, password):
        raise ValueError(
            "Password must contain at least "
            "one lower character, "
            "one upper character, "
            "digit or "
            "special symbol"
        )

    return password


def serialize_dt(dt: datetime.datetime) -> str | None:
    if dt is None:
        return
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


StrongPassword = Annotated[
    str, Field(min_length=6, max_length=32), AfterValidator(valid_password)
]

DateTime = Annotated[
    datetime.datetime | None,
    Field(default=None),
    PlainSerializer(serialize_dt, return_type=str),
]


class AuthUser(CustomModel):
    email: EmailStr
    password: StrongPassword


class AdminUser(AuthUser):
    is_admin: bool = True


class UpdateUser(CustomModel):
    email: Annotated[EmailStr | None, Field(default=None)]
    is_admin: Annotated[bool | None, Field(default=None)]
    password: Annotated[StrongPassword | None, Field(default=None)]


class JWTData(CustomModel):
    user_id: Annotated[int, Field(validation_alias="sub")]
    is_admin: bool = False
    expired_at: Annotated[
        datetime.datetime,
        Field(validation_alias="exp"),
        PlainSerializer(serialize_dt, return_type=str),
    ]


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserResponse(CustomModel):
    id: int
    email: EmailStr
    is_admin: bool = False
    created_at: DateTime
    updated_at: DateTime
