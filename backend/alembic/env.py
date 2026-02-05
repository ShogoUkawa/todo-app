import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

# Import models so Alembic can detect them
import app.infrastructure.database.models  # noqa: F401
from alembic import context
from app.infrastructure.config import settings
from app.infrastructure.database.connection import Base

config = context.config

fileConfig(config.file_config)

target_metadata = Base.metadata


async def run_migrations_online() -> None:
    connectable = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as conn:
        await conn.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: object) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)  # type: ignore[arg-type]

    with context.begin_transaction():
        context.run_migrations()


asyncio.run(run_migrations_online())
