from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from sqlalchemy import text

from src.db import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger("src.main")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    """Verify DB reachability on startup, dispose the engine on shutdown."""
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    logger.info("database connection verified")
    try:
        yield
    finally:
        await engine.dispose()
        logger.info("database engine disposed")


app = FastAPI(
    title="Caching Service",
    version="0.1.0",
    description="Interleaves and caches transformed string lists.",
    lifespan=lifespan,
)