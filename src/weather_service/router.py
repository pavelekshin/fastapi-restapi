import asyncio
from asyncio import Task

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.jwt import parse_jwt_user_data
from src.weather_service.client import Client
from src.weather_service.exceptions import InvalidSearchError
from src.weather_service.helper import cache
from src.weather_service.schemas import (
    Coordinates,
    Geocoding,
    GeocodingAPIResponse,
    Location,
    Weather,
    WeatherAPIResponse,
)

router = APIRouter(
    dependencies=[Depends(BackgroundTasks()), Depends(parse_jwt_user_data)]
)


@router.get(
    "/geocording",
    response_model=GeocodingAPIResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
@cache(seconds=60)
async def get_location(
    request: Request,
    loc: Location = Depends(),
):
    client = Client()
    response: GeocodingAPIResponse = await client.get_location(loc)
    return JSONResponse(content=jsonable_encoder(response))


@router.get(
    "/location",
    response_model=Weather,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
@cache(seconds=60)
async def get_weather_by_location(
    request: Request,
    coordinate: Coordinates = Depends(),
):
    client = Client()
    response: Weather = await client.get_weather(coordinate)
    return JSONResponse(
        content=jsonable_encoder(
            response, exclude_unset=True, exclude_none=True, by_alias=True
        )
    )


@router.get(
    "/weather",
    response_model=WeatherAPIResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
@cache(seconds=60)
async def get_weather_by_location_name(
    request: Request,
    loc: Location = Depends(),
):
    client = Client()
    response: GeocodingAPIResponse = await client.get_location(loc)
    entries: list[Geocoding] = response.entries

    try:
        async with asyncio.TaskGroup() as tg:
            tasks: list[Task] = [
                tg.create_task(
                    client.get_weather(Coordinates(lat=geo.lat, lon=geo.lon)),
                    name=f"Task-{geo.lat},{geo.lon}",
                )
                for geo in entries
            ]
    except ExceptionGroup:
        pass
    except BaseExceptionGroup:
        pass

    responses = [done.result() for done in tasks]

    if len(responses) == 0:
        raise InvalidSearchError("Remote server doesn't provide any results")

    return JSONResponse(
        content=WeatherAPIResponse(entries=responses).model_dump(
            context={}, exclude_unset=True, exclude_none=True, by_alias=True
        )
    )
