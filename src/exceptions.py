from typing import Any

from pydantic import BaseModel

from src.constants import ErrorCode, ErrorMessage


class ErrorItem(BaseModel):
    error_code: str
    error_message: str
    error_detail: Any | None = None


class ErrorResponse(BaseModel):
    error: ErrorItem


class DetailedError(Exception):
    ERROR_MESSAGE = ErrorMessage.INTERNAL_SERVER_ERROR
    ERROR_CODE = ErrorCode.INTERNAL_SERVER_ERROR
    ERROR_DETAIL = None

    def __init__(self, detail=None):
        self.ERROR_DETAIL = detail


class PermissionDeniedError(DetailedError):
    ERROR_MESSAGE = ErrorMessage.PERMISSION_DENIED


class NotFoundError(DetailedError):
    ERROR_MESSAGE = ErrorMessage.NOT_FOUND


class BadRequestError(DetailedError):
    ERROR_MESSAGE = ErrorMessage.BAD_REQUEST


class ExternalError(DetailedError):
    ERROR_MESSAGE = ErrorMessage.EXTERNAL_ERROR


class NotAuthenticatedError(DetailedError):
    ERROR_MESSAGE = ErrorMessage.AUTHENTICATION_ERROR
