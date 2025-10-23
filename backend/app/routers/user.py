from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import database_config
from app.repositories.account import (
    AccountRepository,
)
from app.repositories.user import (
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


router = APIRouter(tags=["users"])


# @router.get(
#     "/samples",
#     response_model=list[SampleResponse],
#     status_code=HTTPStatus.OK.value,
# )
# async def get_samples(
#     service: Annotated[SampleService, Depends(get_sample_service_)],
#     session: Annotated[AsyncSession, Depends(database_config.get_db_session)],
# ) -> list[SampleResponse]:
#     return await service.find_all(session)


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
