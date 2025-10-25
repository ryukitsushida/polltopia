from app.exceptions.base import (
    AppUnauthorizedException,
)


class InvalidCredentialsException(AppUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid credentials provided")


class ExpiredSignatureException(AppUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The token signature has expired")


class InvalidSignatureException(AppUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The token signature is invalid")


class InvalidTokenException(AppUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The token is invalid")
