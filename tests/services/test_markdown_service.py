from changelog_cli.services.markdown_service import create_changelog_markdown
import pytest


def test_create_changelog_markdown():
    sample_entries = {
        "abc123": {
            "hash": "abc123",
            "author": "Test Author",
            "date": "Wed Feb 12 17:32:59 2025 -0600",
            "message": "test commit",
            "changes": {
                "Added": [{"description": "Test feature", "relevance_score": 8}],
                "Fixed": [],
                "Changed": [],
                "Removed": [],
            },
        }
    }

    result = create_changelog_markdown(sample_entries)
    assert "# Changelog 📝" in result
    assert "Test feature" in result
    assert "test commit" in result


def test_create_changelog_markdown_empty():
    result = create_changelog_markdown({})
    assert "# Changelog 📝" in result
    assert "All notable changes" in result
