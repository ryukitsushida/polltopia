class AppException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


# 401
class AppUnauthorizedException(AppException):
    pass


# 409
class AppConflictException(AppException):
    pass
