import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.db.config import database_config
from app.db.seed_data import seed_data
from app.routers import sample


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if "ENV" not in os.environ:
        raise ValueError("ENV environment variable is not set.")

    if os.environ["ENV"] != "dev":
        return
    await database_config.create_tables()
    await seed_data(database_config)
    try:
        yield
    finally:
        await database_config.drop_tables()


app = FastAPI(title="PollTopia API", debug=True, lifespan=lifespan)
app.include_router(sample.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
