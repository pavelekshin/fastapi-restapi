import json
import logging
from functools import wraps

import fastapi.logger
from redis.exceptions import ConnectionError
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import BackgroundTasks

from src.redis import get_by_key, set_redis_key, RedisData

logger = fastapi.logger.logger


def cache(seconds):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            request: Request = kwargs.get("request")
            params = request.query_params
            key = f"{func.__name__}_{params}"
            try:
                redis_data = await get_by_key(key)
            except ConnectionError as er:
                logger.error("Redis error %s:", er)
            else:
                if redis_data:
                    return JSONResponse(content=json.loads(redis_data), status_code=200)

            response: JSONResponse = await func(*args, **kwargs)
            body: bytes = response.body
            task = BackgroundTasks()
            task.add_task(set_redis_key, RedisData(key=key, value=body, ttl=seconds))
            response.background = task
            return response

        return wrapped

    return wrapper
