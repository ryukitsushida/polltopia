from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sample import SampleModel


class SampleRepository:
    # async def create(self, session: AsyncSession, *, name: str, description: str | None) -> SampleModel:
    #     obj = SampleModel(name=name, description=description)
    #     session.add(obj)
    #     await session.flush()
    #     await session.refresh(obj)
    #     return obj

    async def find_all(self, session: AsyncSession) -> list[SampleModel]:
        result = await session.execute(select(SampleModel))

        return list(result.scalars().all())
