import uuid

from src.keys import list_hash, payload_id, string_hash


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


def test_payload_id_format():
    """payload_id returns "<hash1>_<hash2>"."""
    result = payload_id(["a"], ["b"])
    parts = result.split("_")
    assert len(parts) == 2
    assert parts[0] == str(list_hash(["a"]))
    assert parts[1] == str(list_hash(["b"]))


def test_payload_id_distinguishes_pair_order():
    """Swapping list_1 and list_2 changes the payload id."""
    assert payload_id(["a"], ["b"]) != payload_id(["b"], ["a"])


def test_payload_id_deterministic():
    assert payload_id(["a", "b"], ["c", "d"]) == payload_id(["a", "b"], ["c", "d"])