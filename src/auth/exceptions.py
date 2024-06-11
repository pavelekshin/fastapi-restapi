from src.auth.constants import ErrorCode
from src.exceptions import BadRequestError, NotAuthenticatedError, PermissionDeniedError


class EmailTakenError(BadRequestError):
    error_code = ErrorCode.EMAIL_TAKEN


class InvalidEmailError(BadRequestError):
    error_code = ErrorCode.INVALID_USERNAME


class InvalidUserIDError(BadRequestError):
    error_code = ErrorCode.INVALID_USERID


class AuthorizationFailedError(PermissionDeniedError):
    error_code = ErrorCode.AUTHORIZATION_FAILED


class AuthRequiredError(NotAuthenticatedError):
    error_code = ErrorCode.AUTHENTICATION_REQUIRED


class InvalidTokenError(NotAuthenticatedError):
    error_code = ErrorCode.INVALID_TOKEN


class InvalidCredentialsError(NotAuthenticatedError):
    error_code = ErrorCode.INVALID_CREDENTIALS


class FormValidationError(NotAuthenticatedError):
    error_code = ErrorCode.FORM_VALIDATION_FAILED


class RefreshTokenNotValidError(NotAuthenticatedError):
    error_code = ErrorCode.REFRESH_TOKEN_NOT_VALID


class RefreshTokenNotFoundError(NotAuthenticatedError):
    error_code = ErrorCode.REFRESH_TOKEN_REQUIRED
