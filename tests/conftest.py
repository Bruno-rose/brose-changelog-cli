import pytest
from fastapi.testclient import TestClient
from changelog_cli.web.app import app


@pytest.fixture(scope="function")
def sample_commit_info():
    return """commit: abc123
author: Test Author
date: Wed Feb 12 17:32:59 2025 -0600
message: feat: test commit

diff --git a/test.py b/test.py
index abc..def
--- a/test.py
+++ b/test.py
@@ -1,1 +1,2 @@
-old line
+new line
+another line
"""
