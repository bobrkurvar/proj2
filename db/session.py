from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import load_config
from db.models import Base
import asyncio

conf = load_config(r"C:\my_bot\.env")
db_url = str(conf.DATABASE_URL)
engine = create_async_engine(db_url)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_connect():
    async_session = async_sessionmaker(engine)
    async with async_session.begin() as session:
        yield session

if __name__ == "__main__":
    asyncio.run(create_table())