from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_USER_ICON_URL
from app.core.utils.security import get_password_hash
from app.crud.account import AccountCRUD
from app.crud.user import UserCRUD
from app.exceptions.user import EmailConflictException
from app.models.enums import Provider
from app.models.user import UserModel
from app.schemas.user.request import CreateUserRequest
from app.schemas.user.response import CreateUserResponse, MeResponse


class UserService:
    def __init__(self, user_crud: UserCRUD, account_crud: AccountCRUD) -> None:
        self.user_crud = user_crud
        self.account_crud = account_crud

    async def get_me(self, session: AsyncSession, user_id: str) -> MeResponse:
        from uuid import UUID

        uid = UUID(user_id)
        result = await session.get(UserModel, uid)
        if result is None:
            from app.exceptions.auth import InvalidTokenException

            raise InvalidTokenException()

        account = await self.account_crud.find_local_by_user_id(session, uid)
        name = account.name if account else ""
        return MeResponse.from_user_and_account_model(result, name)

    async def create(
        self,
        session: AsyncSession,
        request: CreateUserRequest,
    ) -> CreateUserResponse:
        async with session.begin():
            find_user = await self.user_crud.find_by_email(session, request.email)
            if find_user:
                raise EmailConflictException(request.email)
            user = await self.user_crud.create(
                session,
                email=request.email,
            )
            await self.account_crud.create(
                session,
                user_id=user.id,
                name=request.name,
                provider=Provider.LOCAL,
                hashed_password=get_password_hash(request.password),
                image_url=DEFAULT_USER_ICON_URL,
            )
        return CreateUserResponse.from_user_model(user)
