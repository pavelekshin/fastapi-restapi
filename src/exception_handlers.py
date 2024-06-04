from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.exceptions import (
    AuthorizationFailedError,
    AuthRequiredError,
    EmailTakenError,
    FormValidationError,
    InvalidCredentialsError,
    InvalidTokenError,
    NotAuthenticatedError,
    RefreshTokenNotFoundError,
    RefreshTokenNotValidError,
)
from src.exceptions import ErrorItem, ErrorResponse
from src.weather_service.exceptions import InvalidResponseError, InvalidSearchError
from src.weather_service.exceptions import (
    InvalidTokenError as WeatherServiceInvalidToken,
)


async def email_taken_exception_handler(request: Request, exception: [EmailTakenError]):
    error = ErrorItem(
        error_code=exception.error_code,
        error_message=exception.error_message,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ErrorResponse(error=error), exclude_none=True, exclude_unset=True
        ),
    )


async def authorization_failed_exception_handler(
    request: Request, exception: [AuthorizationFailedError]
):
    error = ErrorItem(
        error_code=exception.error_code,
        error_message=exception.error_message,
    )
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder(
            ErrorResponse(error=error), exclude_none=True, exclude_unset=True
        ),
    )


async def auth_failed_exception_handler(
    request: Request,
    exception: [
        InvalidCredentialsError,
        AuthRequiredError,
        NotAuthenticatedError,
        InvalidTokenError,
        RefreshTokenNotValidError,
        RefreshTokenNotFoundError,
    ],
):
    error = ErrorItem(
        error_code=exception.error_code,
        error_message=exception.error_message,
    )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            ErrorResponse(error=error), exclude_none=True, exclude_unset=True
        ),
        headers={"WWW-Authenticate": "Bearer"},
    )


async def weather_auth_failed_exception_handler(
    request: Request,
    exception: [
        WeatherServiceInvalidToken,
    ],
):
    error = ErrorItem(
        error_code=exception.error_code,
        error_message=exception.error_message,
    )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            ErrorResponse(error=error), exclude_none=True, exclude_unset=True
        ),
    )


async def remote_server_bad_response_failed_exception_handler(
    request: Request, exception: [InvalidResponseError, InvalidSearchError]
):
    error = ErrorItem(
        error_code=exception.error_code,
        error_message=exception.error_message,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ErrorResponse(error=error), exclude_none=True, exclude_unset=True
        ),
    )


async def request_validation_exception_handler(
    request: Request, exception: [RequestValidationError]
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": exception.errors(), "body": exception.body}
        ),
    )


async def form_validation_exception_handler(
    request: Request, exception: [FormValidationError]
):
    return JSONResponse(
        {"error": exception.error_detail}, status_code=status.HTTP_401_UNAUTHORIZED
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(FormValidationError, form_validation_exception_handler)
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(InvalidCredentialsError, auth_failed_exception_handler)
    app.add_exception_handler(AuthRequiredError, auth_failed_exception_handler)
    app.add_exception_handler(NotAuthenticatedError, auth_failed_exception_handler)
    app.add_exception_handler(InvalidTokenError, auth_failed_exception_handler)
    app.add_exception_handler(RefreshTokenNotValidError, auth_failed_exception_handler)
    app.add_exception_handler(RefreshTokenNotFoundError, auth_failed_exception_handler)
    app.add_exception_handler(
        AuthorizationFailedError, authorization_failed_exception_handler
    )
    app.add_exception_handler(EmailTakenError, email_taken_exception_handler)
    app.add_exception_handler(
        InvalidResponseError, remote_server_bad_response_failed_exception_handler
    )
    app.add_exception_handler(
        InvalidSearchError, remote_server_bad_response_failed_exception_handler
    )
    app.add_exception_handler(
        WeatherServiceInvalidToken, weather_auth_failed_exception_handler
    )
