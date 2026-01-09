# routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from database.db import get_db
from health.schemas import PulseSchema, ExistsTables
from management.exceptions.exceptions import (
    CantConnectPostgresHttpException,
    CantCheckMigrationsHttpException,
    CantConnectRedisHttpException,
)

from sqlalchemy.exc import DBAPIError, SQLAlchemyError
import asyncpg
from redisdb.utils import redis_clients

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/pulse/", response_model=PulseSchema)
async def check_pulse():
    return PulseSchema(description="Fastapi alive")


@router.get("/db/", response_model=PulseSchema)
async def check_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return PulseSchema(description="Postgres alive")

    except (DBAPIError, SQLAlchemyError) as e:
        orig = e.orig
        if isinstance(orig, asyncpg.ConnectionDoesNotExistError):
            detail = "Connection was closed unexpectedly. Check if postgres is running and the port is free. Maybe PID already used by other postgres"
        else:
            detail = f"Database error: {str(e)}"
        raise CantConnectPostgresHttpException(e=detail)

    except Exception as e:
        raise CantConnectPostgresHttpException(e=str(e))


@router.get("/migrations/", response_model=ExistsTables)
async def check_migrations(db: AsyncSession = Depends(get_db)):
    try:
        query = text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """
        )
        result = await db.execute(query)
        table_names = [row[0] for row in result.fetchall()]
        return ExistsTables(tables=table_names)
    except Exception as e:
        raise CantCheckMigrationsHttpException(e=str(e))


@router.get("/redis/", response_model=PulseSchema)
async def check_redis():
    try:
        for name, client in redis_clients.items():
            await client.ping()
        return PulseSchema(description="Redis alive")
    except Exception as e:
        raise CantConnectRedisHttpException(e=str(e))
