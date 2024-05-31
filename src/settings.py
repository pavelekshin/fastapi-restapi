from typing import Any

from src.config.config import BaseConfig, PostgreSQL

# default postgresql docker settings
settings = BaseConfig()
db_settings = PostgreSQL(url=str(settings.DATABASE_URL))

app_configs: dict[str, Any] = {"title": "App API", }
app_configs["swagger_ui_parameters"] = {"defaultModelsExpandDepth": -1}  # hide schemas
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
