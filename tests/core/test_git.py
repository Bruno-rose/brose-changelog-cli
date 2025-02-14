import pytest
from changelog_cli.core.git import get_commit_changes, commits_to_generate_changelogs
import subprocess
from unittest.mock import patch, MagicMock


def test_get_commit_changes_success():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0, stdout="Test commit output", stderr=""
        )
        result = get_commit_changes(["abc123"])
        assert result == "Test commit output"


def test_get_commit_changes_failure():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="Error message"
        )
        result = get_commit_changes(["abc123"])
        assert result is None


def test_commits_to_generate_changelogs():
    with patch("changelog_cli.core.git.get_all_main_branch_commits") as mock_all:
        with patch("changelog_cli.core.git.get_commit_hashes_from_json") as mock_json:
            mock_all.return_value = ["commit1", "commit2", "commit3"]
            mock_json.return_value = ["commit1"]
            result = commits_to_generate_changelogs()
            assert result == ["commit2", "commit3"]
