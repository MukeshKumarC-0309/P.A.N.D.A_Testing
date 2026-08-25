"""
CRUD round-trips and schema-behavior checks for the Emergency table.

These exercise the exact SQL the vault functions run (parameterized with
? placeholders), against a temp SQLite vault created from schema.sql.
"""
import sqlite3

import pytest

from panda import vault

INSERT = "insert into Emergency values(?,?,?,?,?,?,?,?)"
ROW = ("P001", "Asha", 30, "O+", "Asthma", "Dr Rao", "9876543210", "{penicillin}")


def test_add_then_view(db):
    db.execute(INSERT, ROW)
    vault.conobj.commit()
    db.execute("select * from Emergency where Patient_ID=?", ("P001",))
    assert db.fetchone() == ROW


def test_edit_updates_field(db):
    db.execute(INSERT, ROW)
    vault.conobj.commit()
    db.execute("update Emergency set Age=? where Patient_ID=?", ("31", "P001"))
    vault.conobj.commit()
    db.execute("select Age from Emergency where Patient_ID=?", ("P001",))
    assert db.fetchone()[0] == 31


def test_delete_removes_row(db):
    db.execute(INSERT, ROW)
    vault.conobj.commit()
    db.execute("delete from Emergency where Patient_ID=?", ("P001",))
    vault.conobj.commit()
    db.execute("select * from Emergency")
    assert db.fetchall() == []


def test_age_stored_as_integer(db):
    # input() hands over the string "41"; the INTEGER affinity coerces it.
    db.execute(INSERT, ("P1", "N", "41", "O+", "x", "d", "1", "n"))
    vault.conobj.commit()
    db.execute("select Age from Emergency where Patient_ID=?", ("P1",))
    stored = db.fetchone()[0]
    assert stored == 41 and isinstance(stored, int)


def test_duplicate_patient_id_rejected(db):
    db.execute(INSERT, ROW)
    vault.conobj.commit()
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(INSERT, ROW)  # PRIMARY KEY collision on Patient_ID


def test_safe_identifier_accepts_and_rejects():
    assert vault._safe_identifier("Emergency") == "Emergency"
    assert vault._safe_identifier("Patient_ID") == "Patient_ID"
    for bad in ("a b", "x'; drop table Emergency", "1abc", "col;--"):
        with pytest.raises(ValueError):
            vault._safe_identifier(bad)
