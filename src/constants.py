from enum import Enum


class Tags(str, Enum):
    AUTH = "Auth"
    ADMIN = "Admin"
    WEATHER = "Weather Service Calls"


class ErrorCode:
    INTERNAL_SERVER_ERROR = "Internal Server error"


class ErrorMessage:
    INTERNAL_SERVER_ERROR = "Internal Server error"
    PERMISSION_DENIED = "Permission denied"
    NOT_FOUND = "Not Found"
    BAD_REQUEST = "Bad Request"
    EXTERNAL_ERROR = "External error, try later"
    AUTHENTICATION_ERROR = "User not authenticated"


class Environment(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)
