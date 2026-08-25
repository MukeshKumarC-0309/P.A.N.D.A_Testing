"""
Shared SQLite connection + first-run bootstrap for PandaVault.

This module owns the database so that any capability can share one open
connection to the single per-device vault file (see config.DB_PATH),
rather than each opening its own. Today the personal-records vault
(panda/vault.py) uses it; a future TDR (threat detection) component can
import the same connection to persist its alerts/incidents in the same
file.

The vault file is created on first run from schema.sql at the repo root.
"""
import sqlite3
from pathlib import Path

from config import DB_PATH

# schema.sql lives at the repo root (one level up from this panda/ package).
# Resolve it from __file__ so it is found regardless of the launch directory.
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema.sql"


def init_db(db_path=DB_PATH):
    """
    Open (and on first run, create) the local SQLite vault.

    Ensures the parent directory exists, connects to the vault file
    (sqlite3 creates it if missing), then runs schema.sql so the built-in
    tables exist as empty tables. CREATE TABLE IF NOT EXISTS makes this
    idempotent and non-destructive: existing user data is never touched.
    Returns the open connection.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn


# The one shared connection/cursor for the process.
connection = init_db()
cursor = connection.cursor()
