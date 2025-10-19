from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sample import SampleRepository
from app.schemas.sample.response import (
    SampleResponse,
)


class SampleService:
    def __init__(self, repo: SampleRepository) -> None:
        self.repo = repo

    async def find_all(self, session: AsyncSession) -> list[SampleResponse]:
        samples = await self.repo.find_all(session)
        return [SampleResponse.to(sample) for sample in samples]
