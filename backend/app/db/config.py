import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseConfig:
    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/polltopia")
        self.engine = create_async_engine(self.database_url, echo=True)
        self.AsyncSessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


database_config = DatabaseConfig()
