from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from http import HTTPStatus

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import setting
from app.core.database import database_config
from app.core.seed_data import seed_data
from app.exceptions.base import (
    AppConflictException,
    AppException,
    AppUnauthorizedException,
)
from app.routers import (
    auth,
    sample,
    user,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    is_dev = setting.app_env == "dev"
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
app_router.include_router(auth.router)
app.include_router(app_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    if isinstance(exc, AppUnauthorizedException):
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={"detail": exc.message},
        )

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
    uvicorn.run(app, host="0.0.0.0", port=setting.app_port, reload=True)
