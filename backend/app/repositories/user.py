from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel


class UserRepository:
    async def find_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> UserModel | None:
        result = await session.execute(select(UserModel).where(UserModel.email == email))
        return result.scalars().first()

    async def create(
        self,
        session: AsyncSession,
        email: EmailStr,
    ) -> UserModel:
        user = UserModel(email=email)
        session.add(user)
        # Ensure PK is available before dependent inserts in the same transaction
        await session.flush()
        return user
