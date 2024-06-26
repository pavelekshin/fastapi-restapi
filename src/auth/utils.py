import secrets
from typing import Any

from src.auth.config import auth_config
from src.settings import settings


def get_refresh_token_settings(
    refresh_token: str,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie = {
        "key": auth_config.REFRESH_TOKEN_KEY,
        "httponly": auth_config.HTTPONLY_COOKIES,
        "samesite": auth_config.SAMESITE_COOKIES,
        "secure": auth_config.SECURE_COOKIES,
        "domain": settings.SITE_DOMAIN,
    }
    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": auth_config.REFRESH_TOKEN_EXP,
    }


def get_token() -> str:
    return secrets.token_hex(settings.TOKEN_SIZE)
