# DECISIONS.md — PandaVault

Guidance and decision record for working in this repo.

## What this project is

PandaVault (P.A.N.D.A) is a **Python CLI desktop app** — a personal
"DBMS for the user." It runs on each user's own device.

- `main.py` — command loop / routing
- `config.py` — env-based config (API keys)
- `panda/auth.py` — password hashing (SHA-256) + vault login
- `panda/vault.py` — the record system (~30 nested functions inside one
  `DATABASE()` function, one per built-in table)
- `panda/utilities.py`, `panda/system.py` — helpers (jokes, weather,
  news, timers, date/time/battery, etc.)

## The database decision (settled)

**Migrating the database from MySQL → SQLite.** Do not re-litigate this.

**Why:** PandaVault is a distributable CLI tool meant to run on each
user's own device as a *private, per-user vault*. MySQL is a server —
it would force every user to install/run MySQL, or make everyone share
one hosted DB (wrong for a private per-user vault). SQLite is embedded
(Python stdlib `sqlite3`): zero-install, one local file per device,
works offline. Exactly right for a per-user personal DBMS.

## The vision to preserve

- The built-in tables (Emergency contacts, Medicine, Grades/Marks,
  Shopping lists, etc.) stay as the provided **schema** but ship with
  **no data** — empty tables created on first run.
- Each user fills their own data and can **create their own tables at
  runtime** (SQLite supports this natively).
- Each device gets its **own local vault file**.

## Settled implementation decisions

- **Vault file location:** the user's home directory —
  `~/.pandavault/vault.db`. Survives regardless of launch directory;
  correct for a "one vault per device" distributable tool.
- **Schema keys:** the reconstructed schema declares `PRIMARY KEY`s
  where the code's logic already implies them (e.g. `Serial_No` on
  `Transaction_History`, so `INSERT OR IGNORE` dedups correctly).
  Column sets and insert order stay identical, so no `INSERT` breaks.

## Tables (curated 2026-08-22)

Curated down to what a private per-user vault actually needs.
- **Kept:** `Emergency` (medical info), `Medicine` (personal pharmacy
  log), `Student_Marks` (exam marksheet).
- **Removed:** `PANDA_Mart`; `Shopping_List`; `Transaction_History` (a
  purchase log that could only be populated from Shopping_List); and
  `Panda_Counter` (a flight timetable — a school-project artifact, not a
  personal record).

To delete a table: remove its `CREATE TABLE` from `schema.sql`, its
functions + routing + header entries from `vault.py`, and any HELP text.

## Gotchas found while reading the code (so they aren't rediscovered)

- **There was no MySQL DDL in the repo.** The schema lived on the
  external MySQL server (`project_Vedha`); the code only *uses* the
  tables. The SQLite schema is therefore **reconstructed** from the
  `INSERT`/`SELECT` statements in `vault.py`.
- **`AUTO_INCREMENT` does not apply here.** Every ID/Serial is typed by
  the user via `input()`, and every `INSERT` supplies all columns
  positionally. Do not add autoincrement PK columns — it would break
  those inserts.
- **MySQL-only syntax that must change for SQLite** (beyond `%s` → `?`):
  - `INSERT IGNORE` → `INSERT OR IGNORE` (`vault.py:582`, `vault.py:796`)
  - `show tables` → `SELECT name FROM sqlite_master WHERE type='table'`
    (`vault.py:725`)
  - `ALTER TABLE t ADD (col varchar(50))` → `ALTER TABLE t ADD COLUMN
    col TEXT` (`vault.py:774`)
  - module-level `mysql.connector.connect(...)` at import
    (`vault.py:21-22`) → `sqlite3.connect(DB_PATH)` + `init_db()`.
- **Pre-existing `.format()`-built SQL (injection pattern)** in
  `PANDA_COUNTER`, `EDIT_COUNTER`, `SEARCH`, `SHOW`, `PRE_SEARCH`
  (e.g. `vault.py:626,649,811,841`) is **out of scope** for this
  migration — it's unrelated to the DB engine. Only touch these where
  they also contain MySQL-only syntax that breaks on SQLite.

## Migration plan (small, reviewable steps)

The connection is module-level and only *connects* at import; table
functions run only when invoked. So migration can proceed table-by-table
— the app still starts while some tables are not yet migrated.

1. Reconstruct the schema → `schema.sql` (7 built-in tables, empty,
   `CREATE TABLE IF NOT EXISTS`, PRIMARY KEYs).
2. `config.py` — drop `DB_HOST/USER/PASSWORD/NAME` and the password
   `raise`; add `DB_PATH`; keep the weather/news keys + checks.
3. Connection + `init_db()` in `vault.py` — `sqlite3.connect(DB_PATH)`,
   run `schema.sql` on first run.
4. Migrate table functions, one table per step (start with Emergency
   as the template): `%s` → `?`.
5. Fix the MySQL-only breakers (`INSERT OR IGNORE`, `sqlite_master`,
   `ALTER TABLE ... ADD COLUMN`).
6. Housekeeping — `requirements.txt` (remove `mysql-connector-python`;
   sqlite3 is stdlib), `.env.example`, `README.md`, `.gitignore`
   (add `*.db`).
7. First-run smoke test — fresh run creates the `.db` with empty tables;
   add/view/delete round-trips on one table.

## Security & correctness hardening (post-migration)

Separate review pass, after the SQLite migration. One fix at a time.

1. **Password hashing → bcrypt** (`panda/auth.py`). Was unsalted
   SHA-256 (fast, no salt, rainbow-table-friendly). Now
   `bcrypt.hashpw`/`bcrypt.checkpw` — per-password random salt,
   deliberately slow. `_hash()` helper removed; `bcrypt` added to
   `requirements.txt`. Old SHA-256 `password.txt` files can't be
   verified by bcrypt, so users just re-set the password (personal
   single-user tool). Also fixed a latent bug in `vault.py`'s EDIT-mode
   gate, which compared the stored hash to raw input (`s == p`) and so
   never worked — now calls `check_password()`.
2. **Password file path** (`panda/auth.py`). Was a relative
   `password.txt` (written/read from the CWD), so launching PANDA from a
   different folder lost the password. Now `PASSWORD_PATH =
   DB_PATH.parent / "password.hash"`, resolved from config so it sits
   next to the vault in `~/.pandavault/` — one password per device,
   independent of launch directory. `password()` ensures the directory
   exists before writing.
3. **`change` crash on fresh install** (`main.py`). `check_password`
   raises `FileNotFoundError` when no password is set yet, but the
   `change` handler didn't catch it — typing "change" before ever
   setting a password threw an unhandled exception. Now wrapped in
   `try/except FileNotFoundError`, mirroring the `vault` handler:
   report it and prompt to set the password.
4. **`.format()` SQL in Search/Show** (`panda/vault.py`: `SEARCH`,
   `SHOW`, `PRE_SEARCH`). Honest nuance: local single-user per-device
   vault, input comes only from the user into their own file, so not a
   live exploit — a best-practice / interview-optics fix. VALUES are now
   bound as `?` parameters; IDENTIFIERS (table/column names, which can't
   be parameterized) are validated with a whitelist (`_safe_identifier`,
   `^[A-Za-z_][A-Za-z0-9_]*$`) before interpolation. `PRE_SEARCH`'s
   table is checked for `header_dictionary` membership (also fixes a
   latent `KeyError` on an unknown table). The "create your own table"
   feature still works. Out of scope: the `.format()` DDL in
   `panda_create` (identifiers only, no values) and the bare `except:`
   blocks.
5. **DRY / cleanup.** The `vault` handler in `main.py` duplicated the
   whole 3-attempt login loop (once in `try`, again in `except`);
   extracted to a single `open_vault()` helper called from both paths.
   `auth.password()` now writes with a `with` block instead of manual
   `open('w+')` + `close()`.

## How to work in this repo

- Read the actual code and verify assumptions against it before proposing.
- Work in the smallest reviewable pieces (one function / small unit).
- Explain in plain language before and after each piece; then stop and
  wait for confirmation. Do not generate the whole migration at once.
