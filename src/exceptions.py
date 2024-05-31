from typing import Any
from pydantic import BaseModel

from src.constants import ErrorCode


class ErrorItem(BaseModel):
    error_code: str
    error_message: str
    error_detail: Any | None = None


class ErrorResponse(BaseModel):
    error: ErrorItem


class DetailedError(Exception):
    error_message = "Internal Server error"
    error_code = "Internal Server error"
    error_detail = None

    def __init__(self, detail=None):
        self.error_detail = detail


class PermissionDenied(DetailedError):
    error_message = "Permission denied"


class NotFound(DetailedError):
    error_message = "Not Found"


class BadRequest(DetailedError):
    error_message = "Bad Request"


class RemoteError(DetailedError):
    error_message = "Remote error, try later"


class NotAuthenticated(DetailedError):
    error_message = "User not authenticated"
