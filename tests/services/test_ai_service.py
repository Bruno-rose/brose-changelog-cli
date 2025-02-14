import pytest
from changelog_cli.services.ai_service import (
    generate_changelog,
    Commit,
    CommitChanges,
    Change,
)
from unittest.mock import patch, MagicMock


# Create a fixture for the test commit info
@pytest.fixture
def test_commit_info():
    return """commit abc123
Author: Test Author
Date: Wed Feb 12 17:32:59 2025 -0600
Message: test commit

    Test commit message

diff --git a/test.py b/test.py
index abc..def 100000
--- a/test.py
+++ b/test.py
@@ -1,1 +1,2 @@
-old line
+new line
+another line"""


@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "message": {
                    "content": """{
    "hash": "abc123",
    "author": "Test Author",
    "date": "Wed Feb 12 17:32:59 2025 -0600",
    "message": "test commit",
    "changes": {
        "Added": [
            {
                "description": "Added a new line and another line to test.py",
                "relevance_score": 4
            }
        ],
        "Fixed": [],
        "Changed": [],
        "Removed": []
    }
}"""
                }
            }
        ]
    }


def test_generate_changelog_success(test_commit_info, mock_openai_response):
    # Create a properly structured mock response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content=mock_openai_response["choices"][0]["message"]["content"]
            )
        )
    ]

    # Patch both the OpenAI client initialization and the environment
    with patch("changelog_cli.services.ai_service.client") as mock_client:
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            result = generate_changelog(test_commit_info)

            # Verify the mock was called correctly
            mock_client.chat.completions.create.assert_called_once()

            # Verify the result
            assert result.hash == "abc123"
            assert result.author == "Test Author"
            assert result.message == "test commit"
            assert result.date == "Wed Feb 12 17:32:59 2025 -0600"
            assert len(result.changes.Added) == 1
            assert (
                result.changes.Added[0].description
                == "Added a new line and another line to test.py"
            )
            assert result.changes.Added[0].relevance_score == 4
            assert not result.changes.Fixed
            assert not result.changes.Changed
            assert not result.changes.Removed


def test_generate_changelog_api_error():
    with patch("changelog_cli.services.ai_service.client") as mock_client:
        # Configure the mock to raise an exception
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            result = generate_changelog("test commit info")

            # Verify error response
            assert result.hash == "error"
            assert result.author == "unknown"
            assert result.date == "unknown"
            assert result.message == "Error generating changelog: API Error"
            assert not result.changes.Added
            assert not result.changes.Fixed
            assert not result.changes.Changed
            assert not result.changes.Removed
