import httpx

from src.settings import settings
from src.weather_service.exceptions import InvalidResponseError, InvalidTokenError
from src.weather_service.schemas import (
    Coordinates,
    GeocodingAPIResponse,
    GeocodingList,
    Location,
    Weather,
)


class Client:
    """
    This is the client to Public APIs service,
    which returns the list of APIs with public access.
    """

    BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    GEO_BASE_URL: str = "http://api.openweathermap.org/geo/1.0/direct"
    APIKEY: str = settings.WEATHER_SERVICE_APIKEY

    @property
    def client(self):
        return httpx.AsyncClient(timeout=5.0)

    async def get_location(self, loc: Location, limit: int = 5) -> GeocodingAPIResponse:
        async with self.client as client:
            params = {
                "q": f"{loc.city},{loc.country}",
                "limit": limit,
                "appid": self.APIKEY,
            }
            response = await client.get(self.GEO_BASE_URL, params=params)
            if not response.is_success:
                if response.status_code == 401:
                    raise InvalidTokenError("Remote client authentication issue")
                raise InvalidResponseError(response.json())

        geo_list = GeocodingList.model_validate_json(response.read())
        return GeocodingAPIResponse(entries=geo_list)

    async def get_weather(
        self, coordinate: Coordinates, units: str = "metric"
    ) -> Weather:
        async with self.client as client:
            params = {
                "lat": f"{coordinate.lat}",
                "lon": f"{coordinate.lon}",
                "units": units,
                "appid": self.APIKEY,
            }
            response = await client.get(self.BASE_URL, params=params)
            if not response.is_success:
                if response.status_code == 401:
                    raise InvalidTokenError("Remote client authentication issue")
                raise InvalidResponseError(response.json())

        return Weather.model_validate_json(response.read())
