import asyncio

from src.transformer import transform


def test_uppercases_ascii():
    assert asyncio.run(transform("hello")) == "HELLO"


def test_uppercases_already_upper():
    assert asyncio.run(transform("HELLO")) == "HELLO"


def test_uppercases_empty():
    assert asyncio.run(transform("")) == ""


def test_uppercases_unicode():
    assert asyncio.run(transform("café")) == "CAFÉ"


def test_zero_latency_returns_input_uppercased():
    assert asyncio.run(transform("x", latency_s=0.0)) == "X"