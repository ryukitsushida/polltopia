from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import AccountModel
from app.models.enums import Provider
from app.models.user import UserModel


class AccountRepository:
    async def find_local_by_email(self, session: AsyncSession, email: str) -> AccountModel | None:
        stmt = (
            select(AccountModel)
            .join(AccountModel.user)
            .where(UserModel.email == email, AccountModel.provider == Provider.LOCAL)
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        session: AsyncSession,
        user_id: UUID,
        name: str,
        provider: Provider,
        provider_id: str | None = None,
        hashed_password: str | None = None,
        image_url: str | None = None,
    ) -> AccountModel:
        account = AccountModel(
            user_id=user_id,
            name=name,
            provider=provider,
            provider_id=provider_id,
            hashed_password=hashed_password,
            image_url=image_url,
        )
        session.add(account)
        await session.flush()
        return account
