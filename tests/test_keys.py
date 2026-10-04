import uuid

from src.keys import list_hash, string_hash


def test_string_hash_returns_uuid():
    assert isinstance(string_hash("anything"), uuid.UUID)


def test_string_hash_deterministic():
    assert string_hash("hello") == string_hash("hello")


def test_string_hash_empty():
    assert string_hash("") == string_hash("")


def test_string_hash_case_sensitive():
    assert string_hash("hello") != string_hash("Hello")


def test_list_hash_returns_uuid():
    assert isinstance(list_hash(["a", "b"]), uuid.UUID)


def test_list_hash_deterministic():
    assert list_hash(["a", "b"]) == list_hash(["a", "b"])


def test_list_hash_empty():
    assert list_hash([]) == list_hash([])


def test_list_hash_order_matters():
    assert list_hash(["a", "b"]) != list_hash(["b", "a"])


def test_list_hash_length_prefixes():
    """['ab','c'] and ['a','bc'] hash differently."""
    assert list_hash(["ab", "c"]) != list_hash(["a", "bc"])