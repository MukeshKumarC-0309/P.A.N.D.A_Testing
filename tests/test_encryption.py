"""
Vault encryption lifecycle tests (panda.db unlock/lock).

Verify that locking writes an encrypted file, unlocking restores the
in-memory data, a wrong password is rejected, and no plaintext leaks
onto disk. Uses tmp_path so the real vault is never touched.
"""
import pytest

from panda import db as dao
from panda import crypto

ROW = ("PX", "Asha", 30, "O+", "Asthma", "Dr Rao", "9876543210", "{pcn}")


def test_lock_then_unlock_roundtrip(db, tmp_path):
    path = tmp_path / "vault.db"
    dao.insert("Emergency", ROW)
    dao.lock("pw", path=path)
    assert path.exists()

    # Wipe memory; unlocking must bring the row back.
    dao.cursor.execute("delete from Emergency")
    dao.connection.commit()
    assert dao.fetch_all("Emergency") == []

    dao.unlock("pw", path=path)
    assert dao.fetch_all("Emergency") == [ROW]


def test_unlock_wrong_password_raises(db, tmp_path):
    path = tmp_path / "vault.db"
    dao.insert("Emergency", ROW)
    dao.lock("pw", path=path)
    with pytest.raises(crypto.BadPassword):
        dao.unlock("wrong-password", path=path)


def test_unlock_missing_file_is_noop(db, tmp_path):
    # First run: no file yet -> unlock leaves the empty in-memory schema.
    dao.unlock("pw", path=tmp_path / "does-not-exist.db")
    assert dao.fetch_all("Emergency") == []


def test_file_has_no_plaintext(db, tmp_path):
    path = tmp_path / "vault.db"
    dao.insert("Emergency", ("SEEKRIT_ID", "ZEDNAME", 1, "O+", "x", "d", "1", "n"))
    dao.lock("pw", path=path)
    blob = path.read_bytes()
    assert b"SEEKRIT_ID" not in blob
    assert b"ZEDNAME" not in blob
