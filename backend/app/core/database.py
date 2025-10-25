from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import setting


class Base(DeclarativeBase):
    pass


class DatabaseConfig:
    def __init__(self) -> None:
        self.database_url = setting.database_url
        self.engine = create_async_engine(self.database_url)
        self.AsyncSessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def get_db_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.AsyncSessionLocal() as session:
            yield session

    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


database_config = DatabaseConfig()
