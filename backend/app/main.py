import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from http import HTTPStatus

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from app.db.config import database_config
from app.db.seed_data import seed_data
from app.exceptions.base import (
    AppConflictException,
    AppException,
)
from app.models import (  # noqa: F401
    AccountModel,
    SampleModel,
    UserModel,
)
from app.routers import (
    sample,
    user,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    if "ENV" not in os.environ:
        raise ValueError("ENV environment variable is not set.")

    is_dev = os.environ["ENV"] == "dev"
    if is_dev:
        await database_config.create_tables()
        await seed_data(database_config)
    try:
        yield
    finally:
        if is_dev:
            await database_config.drop_tables()


app = FastAPI(title="Polltopia API", lifespan=lifespan)

app_router = APIRouter()
app_router.include_router(sample.router)
app_router.include_router(user.router)
app.include_router(app_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    if isinstance(exc, AppConflictException):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={"detail": exc.message},
        )
    else:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
