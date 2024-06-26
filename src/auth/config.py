from src.models.models import CustomSettings


class AuthConfig(CustomSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True
    SAMESITE_COOKIES: str = "none"
    HTTPONLY_COOKIES: bool = True


auth_config = AuthConfig()
