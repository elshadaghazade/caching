from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging
from typing import Annotated

from fastapi import Body, Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import engine, get_db
from src.schemas import PayloadCreateResponse, PayloadRequest, TransformsResponse
from src.services import cache_payload, get_payload

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


@app.post("/payload", response_model=PayloadCreateResponse, status_code=201)
async def post_payload(
    body: Annotated[PayloadRequest, Body(min_length=1)],
    session: AsyncSession = Depends(get_db),
) -> PayloadCreateResponse:
    """Transform and cache the payload. Returns its id for later retrieval."""
    pid = await cache_payload(session, body)
    await session.commit()
    return PayloadCreateResponse(id=pid)


@app.get("/payload/{id}", response_model=TransformsResponse, status_code=200)
async def retrieve_payload(id: int, session: AsyncSession = Depends(get_db)) -> TransformsResponse:
    """Retrieves transformed strings by their id"""
    output = await get_payload(
        session=session,
        id=id
    )
    await session.commit()
    return TransformsResponse(output=output)