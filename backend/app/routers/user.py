from http import HTTPStatus
from typing import Annotated

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
)
from app.services.sample import SampleService


def get_sample_service_() -> SampleService:
    repo = SampleRepository()
    service = SampleService(repo)
    return service


router = APIRouter(tags=["users"])


# @router.get(
#     "/samples",
#     response_model=list[SampleResponse],
#     status_code=HTTPStatus.OK.value,
# )
# async def get_samples(
#     service: Annotated[SampleService, Depends(get_sample_service_)],
#     session: Annotated[AsyncSession, Depends(database_config.get_db_session)],
# ) -> list[SampleResponse]:
#     return await service.find_all(session)


@router.post(
    "/users",
    response_model=CreateSampleResponse,
    status_code=HTTPStatus.CREATED.value,
)
async def create_sample(
    request: CreateSampleRequest,
    service: Annotated[SampleService, Depends(get_sample_service_)],
    session: Annotated[AsyncSession, Depends(database_config.get_db_session)],
) -> CreateSampleResponse:
    return await service.create(session, request)
