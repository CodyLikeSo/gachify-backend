from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from global_config import user, password, host, port, test_database


if not all([user, password, host, port, test_database]):
    raise ValueError("No creds in .env")
if test_database != "test_db":
    raise ValueError("Test database should be named: test_db")

url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{test_database}"

test_engine = create_async_engine(
    url=url,
    echo=True,
)

SessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
