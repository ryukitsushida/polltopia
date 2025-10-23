from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import AccountModel
from app.models.enums import ProviderType


class AccountRepository:
    async def create(
        self,
        session: AsyncSession,
        user_id: UUID,
        name: str,
        provider: ProviderType,
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
