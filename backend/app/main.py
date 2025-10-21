import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from app.common.exceptions import EmailConflictException
from app.db.config import database_config
from app.db.seed_data import seed_data
from app.routers import sample, user


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
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


@app.exception_handler(EmailConflictException)
async def handle_email_conflict(_: Request, exc: EmailConflictException) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
