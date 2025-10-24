from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_USER_ICON_URL
from app.core.utils.security import get_password_hash
from app.crud.account import AccountRepository
from app.crud.user import UserRepository
from app.exceptions.user import EmailConflictException
from app.models.enums import Provider
from app.schemas.user.request import CreateUserRequest
from app.schemas.user.response import CreateUserResponse


class UserService:
    def __init__(self, user_repository: UserRepository, account_repository: AccountRepository) -> None:
        self.user_repository = user_repository
        self.account_repository = account_repository

    # async def find_all(
    #     self,
    #     session: AsyncSession,
    # ) -> list[SampleResponse]:
    #     samples = await self.repo.find_all(session)
    #     return [SampleResponse.from_model(sample) for sample in samples]

    async def create(
        self,
        session: AsyncSession,
        request: CreateUserRequest,
    ) -> CreateUserResponse:
        async with session.begin():
            find_user = await self.user_repository.find_by_email(session, request.email)
            if find_user:
                raise EmailConflictException(request.email)
            user = await self.user_repository.create(
                session,
                email=request.email,
            )
            await self.account_repository.create(
                session,
                user_id=user.id,
                name=request.name,
                provider=Provider.LOCAL,
                hashed_password=get_password_hash(request.password),
                image_url=DEFAULT_USER_ICON_URL,
            )
        return CreateUserResponse.from_model(user)
