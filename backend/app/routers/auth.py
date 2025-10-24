from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database_config
from app.crud.account import AccountRepository
from app.schemas.auth.request import LoginRequest
from app.schemas.auth.response import LoginResponse
from app.services.auth import AuthService

router = APIRouter(tags=["auth"])


def get_auth_service() -> AuthService:
    return AuthService(account_repository=AccountRepository())


@router.post(
    "/auth/login",
    response_model=LoginResponse,
    status_code=HTTPStatus.OK,
)
async def login(
    request: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
    session: Annotated[AsyncSession, Depends(database_config.get_db_session)],
) -> LoginResponse:
    return await service.login(session, request)
