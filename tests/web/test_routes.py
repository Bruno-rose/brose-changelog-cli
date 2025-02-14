from fastapi.testclient import TestClient
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from changelog_cli.web.app import app


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_render_changelog_success(test_client):
    mock_content = "# Test Changelog\n\nTest content"
    with patch("changelog_cli.web.routes.os.path.exists") as mock_exists:
        mock_exists.return_value = True
        with patch(
            "changelog_cli.web.routes.open", mock_open(read_data=mock_content)
        ) as mock_file:
            response = test_client.get("/")
            assert response.status_code == 200
            assert "Test Changelog" in response.text
            mock_exists.assert_called_once()
            mock_file.assert_called_once()


def test_render_changelog_not_found(test_client):
    with patch("changelog_cli.web.routes.os.path.exists") as mock_exists:
        mock_exists.return_value = False
        response = test_client.get("/")

        # Verify response
        assert response.status_code == 200
        assert "<p style='color:red;'>CHANGELOG.md not found!</p>" in response.text

        # Verify mock was called
        mock_exists.assert_called_once()
