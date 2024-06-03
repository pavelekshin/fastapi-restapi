from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as aioredis
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import redis
from src.auth.router import router as auth_router
from src.exception_handlers import register_error_handlers
from src.settings import app_configs, settings
from src.weather_service.router import router as weather_service_router

REDIS_URL = str(settings.REDIS_URL)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    pool = aioredis.ConnectionPool.from_url(
        REDIS_URL,
        max_connections=10,
        decode_responses=True,
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    yield
    await pool.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=None,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(
    weather_service_router,
    prefix="/weather-service",
    tags=["Weather Service Calls"],
)
register_error_handlers(app=app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
