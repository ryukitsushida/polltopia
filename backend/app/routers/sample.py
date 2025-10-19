from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import database_config
from app.repositories.sample import (
    SampleRepository,
)
from app.schemas.sample.request import (
    CreateSampleRequest,
)
from app.schemas.sample.response import (
    CreateSampleResponse,
    SampleResponse,
)
from app.services.sample import SampleService


def get_sample_service_() -> SampleService:
    repo = SampleRepository()
    service = SampleService(repo)
    return service


router = APIRouter(tags=["samples"])


@router.get("/samples")
async def get_samples(
    service: SampleService = Depends(get_sample_service_),
    session: AsyncSession = Depends(database_config.get_db_session),
) -> list[SampleResponse]:
    return await service.find_all(session)


@router.post("/samples", response_model=CreateSampleResponse)
async def create_sample(
    request: CreateSampleRequest,
) -> CreateSampleResponse:
    return CreateSampleResponse(id=1, name=request.name, description=request.description)
