from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from pydantic import BaseModel

from database.db import Base, get_db
from main import app
from database.db_test import test_engine, override_get_db, SessionLocal

from starlette.status import HTTP_201_CREATED, HTTP_200_OK
import pytest


@pytest_asyncio.fixture(scope="function")
async def test_client():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class BasicTests:
    url: str = ""
    create_model: type[BaseModel]

    @staticmethod
    def auto_fill_model(model_cls, **overrides):
        return model_cls(
            **{field: overrides.get(field, field) for field in model_cls.model_fields}
        )

    @property
    def create_data(self):
        return self.auto_fill_model(self.create_model)

    @pytest.mark.asyncio
    async def test_create_object(self, test_client):
        response = await test_client.post(
            url=self.url, json=self.create_data.model_dump()
        )
        assert response.status_code == HTTP_200_OK