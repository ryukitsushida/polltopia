from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database_config
from app.crud.account import (
    AccountRepository,
)
from app.crud.user import (
    UserRepository,
)
from app.schemas.user.request import (
    CreateUserRequest,
)
from app.schemas.user.response import (
    CreateUserResponse,
)
from app.services.user import UserService


def get_service() -> UserService:
    user_repository = UserRepository()
    account_repository = AccountRepository()
    service = UserService(user_repository=user_repository, account_repository=account_repository)
    return service


router = APIRouter(tags=["auth"])


@router.post(
    "/auth/login",
    response_model=CreateUserResponse,
    status_code=HTTPStatus.CREATED.value,
)
async def login(
    request: CreateUserRequest,
    service: Annotated[UserService, Depends(get_service)],
    session: Annotated[AsyncSession, Depends(database_config.get_db_session)],
) -> CreateUserResponse:
    pass
