from app.db.config import DatabaseConfig
from app.models.sample import SampleModel


async def seed_data(db_config: DatabaseConfig) -> None:
    async for session in db_config.get_db_session():
        async with session.begin():
            sample1 = SampleModel(name="1", description="seed 1")
            sample2 = SampleModel(name="2", description="seed 2")
            session.add_all([sample1, sample2])
