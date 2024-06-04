from src.auth.constants import ErrorCode
from src.exceptions import BadRequestError, NotAuthenticatedError, PermissionDeniedError


class EmailTakenError(BadRequestError):
    ERROR_CODE = ErrorCode.EMAIL_TAKEN


class AuthorizationFailedError(PermissionDeniedError):
    ERROR_CODE = ErrorCode.AUTHORIZATION_FAILED


class AuthRequiredError(NotAuthenticatedError):
    ERROR_CODE = ErrorCode.AUTHENTICATION_REQUIRED


class InvalidTokenError(NotAuthenticatedError):
    ERROR_CODE = ErrorCode.INVALID_TOKEN


class InvalidCredentialsError(NotAuthenticatedError):
    ERROR_CODE = ErrorCode.INVALID_CREDENTIALS


class FormValidationError(NotAuthenticatedError):
    ERROR_CODE = ErrorCode.FORM_VALIDATION_FAILED


class RefreshTokenNotValidError(NotAuthenticatedError):
    ERROR_CODE = ErrorCode.REFRESH_TOKEN_NOT_VALID


class RefreshTokenNotFoundError(NotAuthenticatedError):
    ERROR_CODE = ErrorCode.REFRESH_TOKEN_REQUIRED
