from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.exceptions import (
    AuthorizationFailed,
    AuthRequired,
    EmailTaken,
    InvalidCredentials,
    InvalidToken,
    NotAuthenticated,
    RefreshTokenNotFound,
    RefreshTokenNotValid, FormValidationError,
)
from src.weather_service.exceptions import InvalidToken as WeatherServiceInvalidToken
from src.exceptions import ErrorItem, ErrorResponse
from src.weather_service.exceptions import BadResponse, InvalidSearch


async def email_taken_exception_handler(request: Request, exception: [EmailTaken]):
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
        request: Request, exception: [AuthorizationFailed]
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
            InvalidCredentials,
            AuthRequired,
            NotAuthenticated,
            InvalidToken,
            RefreshTokenNotValid,
            RefreshTokenNotFound,
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
        request: Request, exception: [BadResponse, InvalidSearch]
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
    return JSONResponse({"error": exception.error_detail}, status_code=status.HTTP_401_UNAUTHORIZED)


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(FormValidationError, form_validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(InvalidCredentials, auth_failed_exception_handler)
    app.add_exception_handler(AuthRequired, auth_failed_exception_handler)
    app.add_exception_handler(NotAuthenticated, auth_failed_exception_handler)
    app.add_exception_handler(InvalidToken, auth_failed_exception_handler)
    app.add_exception_handler(RefreshTokenNotValid, auth_failed_exception_handler)
    app.add_exception_handler(RefreshTokenNotFound, auth_failed_exception_handler)
    app.add_exception_handler(
        AuthorizationFailed, authorization_failed_exception_handler
    )
    app.add_exception_handler(EmailTaken, email_taken_exception_handler)
    app.add_exception_handler(BadResponse, remote_server_bad_response_failed_exception_handler)
    app.add_exception_handler(InvalidSearch, remote_server_bad_response_failed_exception_handler)
    app.add_exception_handler(WeatherServiceInvalidToken, weather_auth_failed_exception_handler)
