import uuid

from sqlalchemy import Result, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import PayloadRequest
from src.keys import list_hash, string_hash
from src.models import ListCache, StringCache, Transforms
from src.transformer import transform

async def _create_string_cache(
        session: AsyncSession,
        hash: uuid.UUID,
        original_string: str
) -> str:
    transformed = await transform(original_string, latency_s=0.5)
    try:
        await session.execute(
            insert(StringCache).values(
                string_hash=hash,
                transformed_string=transformed,
                original=original_string
            )
        )
    finally:
        return transformed


async def _create_list_cache(
        session: AsyncSession,
        hash: uuid.UUID,
        item: list[str]
) -> None:
    await session.execute(
        insert(ListCache).values(
            list_hash=hash,
            transformed=item
        )
    )

async def _list_cache_lookup(
    session: AsyncSession,
    hashes: list[uuid.UUID],
) -> dict[uuid.UUID, list[str]]:
    """Return {list_hash: transformed} for the rows that exist in list_cache."""
    if not hashes:
        return {}
    result = await session.execute(
        select(ListCache).where(ListCache.list_hash.in_(hashes))
    )
    return {row.list_hash: row.transformed for row in result.scalars()}

async def create_payload(
        session: AsyncSession,
        payload: dict[uuid.UUID, list[str]]
    ) -> int:
    _payload: set[str] = set()
    for _s in payload.values():
        for s in _s:
            _payload.add(s)

    statement = insert(Transforms).values(
        transforms=_payload
    ).returning(Transforms)

    result = await session.execute(statement)

    ret = result.one_or_none()
    if not ret:
        raise Exception('payload could not be saved')
    return ret[0].id


async def cache_payload(
    session: AsyncSession,
    lists: PayloadRequest,
) -> int:
    """Populate the cache for each inner list. Returns the payload id."""
    payload: dict[uuid.UUID, list[str]] = {}

    list_values = lists.values()
    hashes = [list_hash(values) for values in list_values]
    list_cache = await _list_cache_lookup(session, hashes)

    payload.update(list_cache)

    for item, hash in zip(list_values, hashes):
        if list_cache.get(hash):
            continue
        _item: list[str] = []
        for s in item:
            str_hash = string_hash(s)
            result: Result[StringCache] = await session.execute(
                select(StringCache).where(StringCache.string_hash==str_hash).limit(1)
            )

            stringCache = result.one_or_none()

            if not stringCache:
                transformed = await _create_string_cache(
                    session=session,
                    hash=str_hash,
                    original_string=s
                )
            else:
                transformed = stringCache[0].transformed_string

            _item.append(transformed)

        else:
            try:
                await _create_list_cache(
                    session=session,
                    hash=hash,
                    item=_item
                )
            finally:
                payload.update({ hash: _item })

    return await create_payload(
        session=session,
        payload=payload
    )


async def get_payload(session: AsyncSession, id: int) -> str:
    result = await session.execute(select(Transforms).where(Transforms.id==id))

    payload = result.one_or_none()
    if not payload:
        raise Exception("Not found")

    return ", ".join(payload[0].transforms)