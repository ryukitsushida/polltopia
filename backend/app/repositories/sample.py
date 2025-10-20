from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sample import SampleModel


class SampleRepository:
    async def find_all(self, session: AsyncSession) -> list[SampleModel]:
        result = await session.execute(select(SampleModel))

        return list(result.scalars().all())

    async def create(
        self,
        session: AsyncSession,
        name: str,
        description: str | None = None,
    ) -> SampleModel:
        async with session.begin():
            sample = SampleModel(name=name, description=description)
            session.add(sample)
        await session.refresh(sample)
        return sample
