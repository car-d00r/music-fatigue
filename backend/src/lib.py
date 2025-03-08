"""Library functions for the backend."""

import os

import sqlalchemy as sa


def make_db_uri(is_async: bool = False) -> str:
    """Correctly make the database URI."""
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    prefix = "postgresql"
    if is_async:
        prefix = f"{prefix}+asyncpg"

    return f"{prefix}://{user}:{password}@{host}:{port}/postgres"


def create_async_engine() -> sa.engine.base.Engine:
    """Create an async engine."""
    return sa.create_async_engine(make_db_uri())
