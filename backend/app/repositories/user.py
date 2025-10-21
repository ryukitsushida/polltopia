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
        async with session.begin():
            user = UserModel(email=email)
            session.add(user)
        await session.refresh(user)
        return user
