from src.exceptions import ExternalError, NotAuthenticatedError, NotFoundError
from src.weather_service.constants import ErrorCode


class InvalidResponseError(ExternalError):
    ERROR_CODE = ErrorCode.INVALID_RESPONSE


class InvalidTokenError(NotAuthenticatedError):
    ERROR_CODE = ErrorCode.INVALID_TOKEN


class InvalidSearchError(NotFoundError):
    ERROR_CODE = ErrorCode.INVALID_SEARCH
