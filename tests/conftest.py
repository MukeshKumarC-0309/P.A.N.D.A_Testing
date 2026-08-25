"""
Shared pytest setup.

IMPORTANT: the environment must be configured BEFORE anything imports the
package, because config.py validates API keys at import time and vault.py
opens the SQLite connection at import time. conftest.py is imported by
pytest before the test modules, so setting os.environ here (above the
package imports) is what makes that ordering work.

PANDA_DB_PATH is forced to a throwaway temp file so tests never read or
write the real ~/.pandavault vault or password.
"""
import os
import tempfile
from pathlib import Path

_TMPDIR = tempfile.mkdtemp(prefix="pandavault-test-")
os.environ.setdefault("PANDA_WEATHER_API_KEY", "test-key")
os.environ.setdefault("PANDA_NEWS_API_KEY", "test-key")
os.environ["PANDA_DB_PATH"] = str(Path(_TMPDIR) / "vault.db")

import pytest

from panda import vault, auth

BUILTIN_TABLES = ("Emergency", "Medicine", "Student_Marks")


def _wipe():
    for table in BUILTIN_TABLES:
        vault.cur.execute("delete from {}".format(table))
    vault.conobj.commit()


@pytest.fixture
def db():
    """Give a test a clean vault: empty built-in tables before and after."""
    _wipe()
    yield vault.cur
    _wipe()


@pytest.fixture
def clean_password():
    """Ensure no password file exists before/after the test."""
    auth.PASSWORD_PATH.unlink(missing_ok=True)
    yield
    auth.PASSWORD_PATH.unlink(missing_ok=True)
