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
    error_message = ErrorMessage.INTERNAL_SERVER_ERROR
    error_code = ErrorCode.INTERNAL_SERVER_ERROR
    error_detail = None

    def __init__(self, detail=None):
        self.error_detail = detail


class PermissionDeniedError(DetailedError):
    error_message = ErrorMessage.PERMISSION_DENIED


class NotFoundError(DetailedError):
    error_message = ErrorMessage.NOT_FOUND


class BadRequestError(DetailedError):
    error_message = ErrorMessage.BAD_REQUEST


class ExternalError(DetailedError):
    error_message = ErrorMessage.EXTERNAL_ERROR


class NotAuthenticatedError(DetailedError):
    error_message = ErrorMessage.AUTHENTICATION_ERROR
