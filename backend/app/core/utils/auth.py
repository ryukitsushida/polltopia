from datetime import UTC, datetime, timedelta
from typing import Annotated, Any
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import setting
from app.exceptions.auth import (
    ExpiredSignatureException,
    InvalidSignatureException,
    InvalidTokenException,
)


def create_access_token(subject: str) -> str:
    now = datetime.now(UTC)
    exp = now + (timedelta(minutes=setting.jwt_access_token_expire_minutes))
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    token: str = jwt.encode(payload, setting.jwt_secret_key, algorithm=setting.jwt_algorithm)
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(token, setting.jwt_secret_key, algorithms=[setting.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureException() from None
    except jwt.InvalidSignatureError:
        raise InvalidSignatureException() from None
    except jwt.PyJWTError:
        raise InvalidTokenException() from None
    return payload


security = HTTPBearer()


def get_current_user_id(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> UUID:
    token = credentials.credentials
    payload = decode_access_token(token)
    sub = payload.get("sub")
    if not sub:
        raise InvalidTokenException()
    return UUID(str(sub))
