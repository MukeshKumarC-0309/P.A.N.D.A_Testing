"""
Data-access helper tests (panda.db).

These exercise the shared DAO used by the vault today and TDR later:
identifier validation, parameter-bound values, and the CRUD helpers,
against the temp vault created by conftest. The `db` fixture wipes the
built-in tables around each test.
"""
import sqlite3

import pytest

from panda import db as dao

ROW = ("P001", "Asha", 30, "O+", "Asthma", "Dr Rao", "9876543210", "{pcn}")


def test_insert_and_fetch_all(db):
    dao.insert("Emergency", ROW)
    assert dao.fetch_all("Emergency") == [ROW]


def test_fetch_where_binds_value(db):
    dao.insert("Emergency", ROW)
    assert dao.fetch_where("Emergency", "Patient_ID", "P001") == [ROW]
    assert dao.fetch_where("Emergency", "Patient_ID", "nope") == []


def test_update(db):
    dao.insert("Emergency", ROW)
    affected = dao.update("Emergency", "Age", 31, "Patient_ID", "P001")
    assert affected == 1
    assert dao.fetch_where("Emergency", "Patient_ID", "P001")[0][2] == 31


def test_delete(db):
    dao.insert("Emergency", ROW)
    assert dao.delete("Emergency", "Patient_ID", "P001") == 1
    assert dao.fetch_all("Emergency") == []


def test_insert_or_ignore_dedupes_on_primary_key(db):
    dao.insert("Emergency", ROW)
    with pytest.raises(sqlite3.IntegrityError):
        dao.insert("Emergency", ROW)              # duplicate PK -> raises
    dao.insert("Emergency", ROW, or_ignore=True)  # duplicate PK -> skipped
    assert len(dao.fetch_all("Emergency")) == 1


def test_injection_identifier_rejected(db):
    for bad in ("x; drop table Emergency", "a b", "1abc"):
        with pytest.raises(ValueError):
            dao.fetch_all(bad)
        with pytest.raises(ValueError):
            dao.fetch_where("Emergency", bad, "x")


def test_injection_value_is_inert(db):
    dao.insert("Emergency", ROW)
    # A classic payload as a VALUE matches nothing (bound as a literal).
    assert dao.fetch_where("Emergency", "Name", "' OR '1'='1") == []
