from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel


class UserCRUD:
    async def find_by_email(
        self,
        session: AsyncSession,
        email: EmailStr,
    ) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        session: AsyncSession,
        email: EmailStr,
    ) -> UserModel:
        user = UserModel(email=email)
        session.add(user)
        await session.flush()
        return user
