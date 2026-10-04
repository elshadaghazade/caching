from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from src.db import get_db
from src.main import app


def test_post_payload_rejects_empty_dict():
    client = TestClient(app)
    response = client.post("/payload", json={})
    assert response.status_code == 422


def test_post_payload_rejects_non_dict():
    client = TestClient(app)
    response = client.post("/payload", json=["a", "b"])
    assert response.status_code == 422


def test_post_payload_rejects_non_list_value():
    client = TestClient(app)
    response = client.post("/payload", json={"a": "not a list"})
    assert response.status_code == 422


@patch("src.main.cache_payload", new_callable=AsyncMock)
def test_post_payload_accepts_single_entry(mock_cache):
    mock_cache.return_value = 1
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.post("/payload", json={"only": ["a", "b"]})
        assert response.status_code == 201
        assert response.json()["id"] == 1
        mock_cache.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@patch("src.main.cache_payload", new_callable=AsyncMock)
def test_post_payload_accepts_varying_inner_sizes(mock_cache):
    mock_cache.return_value = 7
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.post(
            "/payload",
            json={"short": ["a"], "long": ["b", "c", "d"]},
        )
        assert response.status_code == 201
        assert response.json()["id"] == 7
    finally:
        app.dependency_overrides.clear()


@patch("src.main.cache_payload", new_callable=AsyncMock)
def test_post_payload_happy_path(mock_cache):
    mock_cache.return_value = 42
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.post(
            "/payload",
            json={
                "list_1": ["first string", "second string", "third string"],
                "list_2": ["other string", "another string", "last string"],
            },
        )
        assert response.status_code == 201
        body = response.json()
        assert body["id"] == 42
        assert "message" in body
    finally:
        app.dependency_overrides.clear()


@patch("src.main.cache_payload", new_callable=AsyncMock)
def test_post_payload_passes_dict_to_service(mock_cache):
    mock_cache.return_value = 1
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.post("/payload", json={"a": ["x", "y"], "c": ["z"]})
        assert response.status_code == 201
        args, _ = mock_cache.call_args
        # First arg is the session, second is the dict body
        assert args[1] == {"a": ["x", "y"], "c": ["z"]}
    finally:
        app.dependency_overrides.clear()


@patch("src.main.cache_payload", new_callable=AsyncMock)
def test_post_payload_response_includes_confirmation(mock_cache):
    mock_cache.return_value = 99
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.post("/payload", json={"a": ["x"]})
        body = response.json()
        assert body["message"]
    finally:
        app.dependency_overrides.clear()