from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

DATABASE_URL = (
    "postgresql+asyncpg://"
    "customerpulse:customerpulse@localhost:5436/customerpulse"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session