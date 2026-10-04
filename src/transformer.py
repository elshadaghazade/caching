import asyncio


async def transform(s: str, latency_s: float = 0.001) -> str:
    """Pretend to call an external service that uppercases its input.

    latency_s is configurable so tests can run with 0.0.
    """
    if latency_s > 0:
        await asyncio.sleep(latency_s)
    return s.upper()