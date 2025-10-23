class AppException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class AppConflictException(AppException):
    pass
