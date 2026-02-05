import os
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.infrastructure.database.models  # noqa: F401 — register models with Base
from app.infrastructure.database.connection import Base, get_session
from app.main import app

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+asyncpg://dev:devpassword@localhost:5433/todo_db_test"
)

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=pool.NullPool)
TestSession = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_session() -> AsyncIterator[AsyncSession]:
    async with TestSession() as session:
        async with session.begin():
            yield session


@pytest.fixture(autouse=True)
async def prepare_database() -> AsyncIterator[None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
