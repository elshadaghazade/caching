import asyncio

import pytest

from src.services import get_payload


class _ScalarResult:
    def __init__(self, value):
        self._value = value

    def one_or_none(self):
        return self._value


class _Row:
    def __init__(self, transforms):
        self.transforms = transforms

    def __getitem__(self, key):
        if key == 0:
            return self
        raise IndexError(key)


class _Session:
    def __init__(self, value):
        self._value = value
        self.executed_with = None

    async def execute(self, statement):
        self.executed_with = statement
        return _ScalarResult(self._value)


def test_get_payload_joins_with_commas():
    session = _Session(_Row(transforms=["FIRST", "SECOND", "THIRD"]))
    assert asyncio.run(get_payload(session, id=123)) == "FIRST, SECOND, THIRD"


def test_get_payload_single_entry():
    session = _Session(_Row(transforms=["ONLY"]))
    assert asyncio.run(get_payload(session, id=1)) == "ONLY"


def test_get_payload_empty_transforms():
    session = _Session(_Row(transforms=[]))
    assert asyncio.run(get_payload(session, id=5)) == ""


def test_get_payload_missing_raises():
    session = _Session(None)
    with pytest.raises(Exception):
        asyncio.run(get_payload(session, id=999))