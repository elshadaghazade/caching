import hashlib
import uuid


def string_hash(s: str) -> uuid.UUID:
    """blake2b of the utf-8 bytes, packed into a UUID."""
    return uuid.UUID(
        bytes=hashlib.blake2b(s.encode("utf-8"), digest_size=16).digest()
    )


def list_hash(items: list[str]) -> uuid.UUID:
    """Length-prefixed blake2b over a list of strings, packed into a UUID.

    The 4-byte big-endian length prefix per item disambiguates where each
    string ends, so e.g. ["ab", "c"] and ["a", "bc"] hash differently.
    """
    h = hashlib.blake2b(digest_size=16)
    for s in items:
        encoded = s.encode("utf-8")
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
    return uuid.UUID(bytes=h.digest())