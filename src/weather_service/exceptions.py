from src.exceptions import NotAuthenticated, NotFound, RemoteError
from src.weather_service.constants import ErrorCode


class InvalidResponse(RemoteError):
    error_code = ErrorCode.INVALID_RESPONSE


class InvalidToken(NotAuthenticated):
    error_code = ErrorCode.INVALID_TOKEN


class InvalidSearch(NotFound):
    error_code = ErrorCode.INVALID_SEARCH
