from functools import wraps

from fastapi import BackgroundTasks
from fastapi.logger import logger
from redis.exceptions import ConnectionError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.redis import RedisData, get_by_key, set_redis_key


def cache(seconds):
    def wrapper(func):
        @wraps(func)
        async def wrapped(request: Request, *args, **kwargs):
            if not request:
                return

            params = request.query_params
            key = f"{func.__name__}_{params}"

            try:
                redis_data = await get_by_key(key)
            except ConnectionError as er:
                logger.error("Redis error %s:", er)
            else:
                if redis_data:
                    return Response(
                        content=redis_data,
                        status_code=200,
                        media_type="application/json",
                    )

            response: JSONResponse = await func(request, *args, **kwargs)
            body: bytes = response.body
            task = BackgroundTasks()
            task.add_task(set_redis_key, RedisData(key=key, value=body, ttl=seconds))
            response.background = task
            return response

        return wrapped

    return wrapper
