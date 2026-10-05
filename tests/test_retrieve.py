from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from src.db import get_db
from src.main import app


@patch("src.main.get_payload", new_callable=AsyncMock)
def test_retrieve_payload_happy_path(mock_get):
    mock_get.return_value = "FIRST, SECOND, THIRD"
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.get("/payload/1")
        assert response.status_code == 200
        assert response.json() == {"output": "FIRST, SECOND, THIRD"}
        mock_get.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()


@patch("src.main.get_payload", new_callable=AsyncMock)
def test_retrieve_payload_passes_id_to_service(mock_get):
    mock_get.return_value = "ONLY"
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.get("/payload/42")
        assert response.status_code == 200
        _, kwargs = mock_get.call_args
        assert kwargs["session"] is session
        assert kwargs["id"] == 42
    finally:
        app.dependency_overrides.clear()


@patch("src.main.get_payload", new_callable=AsyncMock)
def test_retrieve_payload_rejects_non_int(mock_get):
    mock_get.return_value = "X"
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.get("/payload/not-an-int")
        assert response.status_code == 422
        mock_get.assert_not_awaited()
    finally:
        app.dependency_overrides.clear()


@patch("src.main.get_payload", new_callable=AsyncMock)
def test_retrieve_payload_empty_output(mock_get):
    mock_get.return_value = ""
    session = AsyncMock()
    app.dependency_overrides[get_db] = lambda: session
    try:
        client = TestClient(app)
        response = client.get("/payload/7")
        assert response.status_code == 200
        assert response.json() == {"output": ""}
    finally:
        app.dependency_overrides.clear()