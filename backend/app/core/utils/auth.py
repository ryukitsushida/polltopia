import os
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.exceptions.auth import (
    ExpiredSignatureException,
    InvalidSignatureException,
    InvalidTokenException,
)

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-prod")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "30"))


def create_access_token(subject: str) -> str:
    now = datetime.now(UTC)
    exp = now + (timedelta(minutes=JWT_EXPIRES_MIN))
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    token: str = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureException() from None
    except jwt.InvalidSignatureError:
        raise InvalidSignatureException() from None
    except jwt.PyJWTError:
        raise InvalidTokenException() from None
    return payload
