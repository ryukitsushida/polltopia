from app.exceptions.base import (
    AppConflictException,
)


class EmailConflictException(AppConflictException):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"Email already exists: {email}")
