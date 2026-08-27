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
import re
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
    conn.execute("PRAGMA foreign_keys = ON")  # enforce FKs (future TDR tables)
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn


# The one shared connection/cursor for the process.
connection = init_db()
cursor = connection.cursor()


# ---------------------------------------------------------------------------
# Data-access helpers.
#
# SQL parameters (?) can bind VALUES but never IDENTIFIERS (table/column
# names). These helpers bind every value as a parameter and validate every
# identifier against a strict whitelist, so callers (the vault today, TDR
# tomorrow) get a safe, DRY query surface instead of hand-writing SQL.
# ---------------------------------------------------------------------------

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def safe_identifier(name):
    """Return name if it is a valid SQL identifier, else raise ValueError.

    A valid identifier is a letter/underscore followed by any number of
    letters, digits, or underscores — so quotes, spaces, semicolons and
    other injection vectors are rejected. Identifiers cannot be bound as
    parameters, so this validation is how table/column names are made safe.
    """
    if _IDENTIFIER_RE.match(name):
        return name
    raise ValueError("Invalid identifier: {!r}".format(name))


def fetch_all(table, order_by=None):
    """Return all rows of a table, optionally ordered by a column."""
    sql = "select * from {}".format(safe_identifier(table))
    if order_by is not None:
        sql += " order by {}".format(safe_identifier(order_by))
    return cursor.execute(sql).fetchall()


def fetch_where(table, column, value):
    """Return rows of a table where column == value (value is bound)."""
    sql = "select * from {} where {} = ?".format(
        safe_identifier(table), safe_identifier(column))
    return cursor.execute(sql, (value,)).fetchall()


def insert(table, values, or_ignore=False):
    """Insert one row (all columns, positional). Returns rows affected.

    or_ignore=True uses INSERT OR IGNORE, so a row that would violate a
    UNIQUE/PRIMARY KEY constraint is skipped instead of raising.
    """
    verb = "insert or ignore into" if or_ignore else "insert into"
    placeholders = ",".join(["?"] * len(values))
    sql = "{} {} values ({})".format(verb, safe_identifier(table), placeholders)
    with connection:
        cursor.execute(sql, tuple(values))
    return cursor.rowcount


def update(table, set_column, value, where_column, where_value):
    """Set one column where another column matches. Returns rows affected."""
    sql = "update {} set {} = ? where {} = ?".format(
        safe_identifier(table), safe_identifier(set_column),
        safe_identifier(where_column))
    with connection:
        cursor.execute(sql, (value, where_value))
    return cursor.rowcount


def delete(table, column, value):
    """Delete rows where column == value (value is bound). Returns count."""
    sql = "delete from {} where {} = ?".format(
        safe_identifier(table), safe_identifier(column))
    with connection:
        cursor.execute(sql, (value,))
    return cursor.rowcount
