from src.exceptions import ExternalError, NotAuthenticatedError, NotFoundError
from src.weather_service.constants import ErrorCode


class InvalidResponseError(ExternalError):
    error_code = ErrorCode.INVALID_RESPONSE


class InvalidTokenError(NotAuthenticatedError):
    error_code = ErrorCode.INVALID_TOKEN


class InvalidSearchError(NotFoundError):
    error_code = ErrorCode.INVALID_SEARCH
