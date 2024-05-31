from src.auth.constants import ErrorCode
from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied

REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."


class EmailTaken(BadRequest):
    error_code = ErrorCode.EMAIL_TAKEN


class AuthorizationFailed(PermissionDenied):
    error_code = ErrorCode.AUTHORIZATION_FAILED


class AuthRequired(NotAuthenticated):
    error_code = ErrorCode.AUTHENTICATION_REQUIRED


class InvalidToken(NotAuthenticated):
    error_code = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    error_code = ErrorCode.INVALID_CREDENTIALS


class RefreshTokenNotValid(NotAuthenticated):
    error_code = ErrorCode.REFRESH_TOKEN_NOT_VALID


class RefreshTokenNotFound(NotAuthenticated):
    error_code = ErrorCode.REFRESH_TOKEN_REQUIRED
