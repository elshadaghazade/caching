"""Async SQLAlchemy wiring: engine, session factory, declarative base."""
from collections.abc import AsyncGenerator
import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import AsyncAdaptedQueuePool

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg_async://cache:cache@postgres:5432/cache",
)
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() in ("1", "true", "yes")

engine = create_async_engine(
    DATABASE_URL,
    echo=DATABASE_ECHO,
    pool_pre_ping=True,
    poolclass=AsyncAdaptedQueuePool,
)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency. Yields a session, closes it after the request."""
    async with SessionLocal() as session:
        yield session