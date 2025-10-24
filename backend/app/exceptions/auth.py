from app.exceptions.base import (
    AppUnauthorizedException,
)


class ExpiredSignatureException(AppUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The token signature has expired")


class InvalidSignatureException(AppUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The token signature is invalid")


class InvalidTokenException(AppUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The token is invalid")
