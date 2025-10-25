
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils.auth import create_access_token
from app.core.utils.security import verify_password
from app.crud.account import AccountRepository
from app.exceptions.auth import InvalidCredentialsException
from app.schemas.auth.request import LoginRequest
from app.schemas.auth.response import LoginResponse


class AuthService:
    def __init__(self, account_repository: AccountRepository) -> None:
        self.account_repository = account_repository

    async def login(self, session: AsyncSession, request: LoginRequest) -> LoginResponse:
        account = await self.account_repository.find_local_by_email(session, request.email)
        if not account or not account.hashed_password:
            raise InvalidCredentialsException()
        if not verify_password(request.password, account.hashed_password):
            raise InvalidCredentialsException()

        subject = str(account.user_id)
        token = create_access_token(subject)
        return LoginResponse(access_token=token, token_type="bearer")
