from http import HTTPStatus
from typing import Annotated, cast
from uuid import UUID
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database_config
from app.core.utils.auth import decode_access_token
from app.crud.account import (
    AccountCRUD,
)
from app.crud.user import (
    UserCRUD,
)
from app.schemas.user.request import (
    CreateUserRequest,
)
from app.schemas.user.response import (
    CreateUserResponse,
    MeResponse,
)
from app.services.user import UserService


def get_service() -> UserService:
    user_crud = UserCRUD()
    account_crud = AccountCRUD()
    service = UserService(user_crud=user_crud, account_crud=account_crud)
    return service


router = APIRouter(tags=["users"])

security = HTTPBearer()


def _get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    payload = decode_access_token(token)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Invalid token")
    _ = UUID(str(sub))
    return cast(str, sub)


@router.get(
    "/users/me",
    response_model=MeResponse,
    status_code=HTTPStatus.OK.value,
)
async def get_me(
    service: Annotated[UserService, Depends(get_service)],
    session: Annotated[AsyncSession, Depends(database_config.get_db_session)],
    user_id: Annotated[str, Depends(_get_current_user_id)],
) -> MeResponse:
    return await service.get_me(session, user_id)


@router.post(
    "/users",
    response_model=CreateUserResponse,
    status_code=HTTPStatus.CREATED.value,
)
async def create_user(
    request: CreateUserRequest,
    service: Annotated[UserService, Depends(get_service)],
    session: Annotated[AsyncSession, Depends(database_config.get_db_session)],
) -> CreateUserResponse:
    return await service.create(session, request)
