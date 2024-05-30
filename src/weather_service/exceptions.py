from src.weather_service.constants import ErrorCode
from src.exceptions import BadRequest, NotAuthenticated, NotFound


class InvalidResponse(BadRequest):
    DETAIL = ErrorCode.INVALID_RESPONSE


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidSearch(NotFound):
    DETAIL = ErrorCode.INVALID_SEARCH
