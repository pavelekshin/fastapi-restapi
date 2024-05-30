import asyncio
from asyncio import Task

from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import JWTData
from src.weather_service.client import Client
from src.weather_service.exceptions import InvalidSearch
from src.weather_service.helper import cache
from src.weather_service.schemas import (
    GeocodingAPIResponse,
    Location,
    Coordinates,
    Geocoding,
    WeatherAPIResponse, Weather
)

router = APIRouter(dependencies=[Depends(BackgroundTasks()), ])


@router.get(
    '/api/location/',
    response_model=GeocodingAPIResponse,
    response_model_exclude_none=True,
)
@cache(seconds=60)
async def get_location(
        request: Request,
        loc: Location = Depends(),
):
    client = Client()
    response: GeocodingAPIResponse = await client.get_location(loc)
    return JSONResponse(content=response.model_dump())


@router.get(
    '/api/weather_by_location/',
    response_model=Weather,
    response_model_exclude_none=True,
)
@cache(seconds=60)
async def get_weather_by_location(
        request: Request,
        coordinate: Coordinates = Depends(),
):
    client = Client()
    response: Weather = await client.get_weather(coordinate)
    return JSONResponse(content=response.model_dump(
        exclude_unset=True,
        exclude_none=True,
        by_alias=True
    ))


@router.get(
    '/api/weather_by_name/',
    response_model=WeatherAPIResponse,
    response_model_exclude_none=True,
)
@cache(seconds=60)
async def get_weather_by_location_name(
        request: Request,
        loc: Location = Depends(),
):
    geo: Geocoding
    client = Client()
    entries: GeocodingAPIResponse = await client.get_location(loc)

    try:
        async with asyncio.TaskGroup() as tg:
            tasks: list[Task] = [
                tg.create_task(client.get_weather(Coordinates(lat=geo.lat, lon=geo.lon)),
                               name=f"Task-{geo.lat},{geo.lon}")
                for geo in entries.entries
            ]
    except ExceptionGroup:
        pass
    except BaseExceptionGroup:
        pass

    responses = [done.result() for done in tasks]

    if len(responses) == 0:
        raise InvalidSearch()

    return JSONResponse(
        content=WeatherAPIResponse(entries=responses).model_dump(
            context={},
            exclude_unset=True,
            exclude_none=True,
            by_alias=True),
        status_code=status.HTTP_200_OK)
