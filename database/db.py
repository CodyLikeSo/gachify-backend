from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from global_config import user, password, host, port, database


if not all([user, password, host, port, database]):
    raise ValueError("No creds in .env")

url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

Base = declarative_base()

engine = create_async_engine(
    pool_pre_ping=True,
    url=url,
    echo=True,
)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    async with SessionLocal() as db:
        yield db