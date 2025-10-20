from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sample import SampleRepository
from app.schemas.sample.request import (
    CreateSampleRequest,
)
from app.schemas.sample.response import (
    CreateSampleResponse,
    SampleResponse,
)


class SampleService:
    def __init__(self, repo: SampleRepository) -> None:
        self.repo = repo

    async def find_all(
        self,
        session: AsyncSession,
    ) -> list[SampleResponse]:
        samples = await self.repo.find_all(session)
        return [SampleResponse.from_model(sample) for sample in samples]

    async def create(
        self,
        session: AsyncSession,
        request: CreateSampleRequest,
    ) -> CreateSampleResponse:
        sample = await self.repo.create(
            session,
            name=request.name,
            description=request.description if request.description else None,
        )
        return CreateSampleResponse.from_model(sample)
