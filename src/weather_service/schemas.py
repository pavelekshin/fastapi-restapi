import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    Field,
    PlainSerializer,
    RootModel,
    computed_field,
    field_serializer,
    model_serializer,
)
from pydantic_core.core_schema import (
    FieldSerializationInfo,
    SerializationInfo,
    SerializerFunctionWrapHandler,
)
from pydantic_extra_types.coordinate import Latitude, Longitude
from pydantic_extra_types.country import CountryAlpha2

from src.models.models import CustomModel


def convert_datetime_to_localtime(
    dt: datetime.datetime, offset: datetime.timedelta
) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.astimezone(datetime.timezone(offset)).strftime("%Y-%m-%dT%H:%M:%S%z")


def serialize_dt(value: datetime.datetime, info: FieldSerializationInfo):
    offset = datetime.timedelta(seconds=0)
    if info.context:
        offset = info.context.get("offset")
    return convert_datetime_to_localtime(value, offset)


LocalDateTime = Annotated[datetime.datetime, PlainSerializer(serialize_dt)]


class Coordinates(BaseModel):
    lon: Longitude
    lat: Latitude


class Wind(BaseModel):
    speed: float | None = None
    deg: int | None = None
    gust: float | None = None


class MainTemp(BaseModel):
    temp: float | None
    feels_like: float | None
    temp_min: float | None
    temp_max: float | None
    pressure: int | None = None
    humidity: int | None = None
    sea_level: int | None = None
    grnd_level: int | None = None


class Sys(CustomModel):
    type: int | None = None
    id: int | None = None
    country: CountryAlpha2 | None = None
    sunrise: LocalDateTime
    sunset: LocalDateTime


class Clouds(BaseModel):
    all: int


class Rain(BaseModel):
    one_hour: float | None = Field(alias="1h", default=None)
    three_hour: float | None = Field(alias="3h", default=None)


class Snow(BaseModel):
    one_hour: float | None = Field(alias="1h", default=None)
    three_hour: float | None = Field(alias="3h", default=None)


class Weather(CustomModel):
    coord: Coordinates
    base: str
    main: MainTemp
    visibility: int | None = None
    wind: Wind
    clouds: Clouds | None = None
    rain: Rain | None = None
    snow: Snow | None = None
    dt: LocalDateTime
    sys: Sys
    timezone: datetime.timedelta = Field(alias="offset_seconds")
    id: int
    name: str
    cod: int

    @computed_field
    @property
    def offset_utc(self) -> str:
        return str(datetime.timezone(self.timezone))

    @field_serializer("timezone")
    def serialize_timezone(self, value: datetime.timedelta):
        return int(value.seconds)

    @model_serializer(mode="wrap")
    def serialize_model(
        self, serializer: SerializerFunctionWrapHandler, info: SerializationInfo
    ):
        if isinstance(info.context, dict):
            info.context["offset"] = self.timezone
        return serializer(self)


class Location(BaseModel):
    city: str
    state: str | None = Field(default=None, description="Used only for US")
    country: str = "RU"


class LocalsName(BaseModel):
    ru: str | None = None
    en: str | None = None


class Geocoding(BaseModel):
    name: str
    local_names: LocalsName | None = None
    lat: Latitude
    lon: Longitude
    country: CountryAlpha2
    state: str | None = None


class GeocodingList(RootModel):
    root: list[Geocoding]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)


class GeocodingAPIResponse(BaseModel):
    entries: GeocodingList

    @computed_field
    @property
    def count(self) -> int:
        return len(self.entries)


class WeatherAPIResponse(BaseModel):
    entries: list[Weather]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.entries)
