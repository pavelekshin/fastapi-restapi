from src.weather_service.constants import ErrorCode
from src.exceptions import RemoteError, NotAuthenticated, NotFound


class BadResponse(RemoteError):
    error_code = ErrorCode.INVALID_RESPONSE


class InvalidToken(NotAuthenticated):
    error_code = ErrorCode.INVALID_TOKEN


class InvalidSearch(NotFound):
    error_code = ErrorCode.INVALID_SEARCH
