# P.A.N.D.A — Security Review & Restructure

A revisit of a 12th-grade school project: a Python CLI assistant with a
local record management system ("PandaVault"). This version removes the
games/arcade module, fixes several real security and correctness issues
found during review, and migrates the database from MySQL to embedded
SQLite so the app is a zero-install, offline, per-user tool — using
skills developed since the original was built.

**Original project:** built with three teammates (Pranav, Vaishanth,
Gautam) for a school board exam project. **My primary contribution**
was the core assistant framework, authentication, and the PandaVault
database system; teammates contributed the games/arcade module, which
has been removed in this version.

## What changed, and why

### 1. Passwords were stored in plaintext — now hashed
The original `password()` function wrote the user's password directly
to `password.txt` with no hashing. Anyone with file access could read
it directly. Fixed by hashing with SHA-256 before storage, and
comparing hashes (never raw text) at login. See `panda/auth.py`.

### 2. Three hardcoded credentials in source code — now environment variables
The original code had a MySQL password, an OpenWeatherMap API key, and
a NewsAPI key all hardcoded directly in the source. This means anyone
who ever saw the code (or a public repo, had this been pushed) had
the credentials too. All three now load from environment variables via
`config.py`, with a `.env.example` template and `.env` gitignored.

### 3. Wrong exception type being caught
`remember()` and the vault login flow both used `except RuntimeError`
to catch what is actually a missing-file case. This silently worked
by accident in some Python versions/setups but is the wrong exception
class — the correct one is `FileNotFoundError`. Fixed in both places.

### 4. Off-by-one in the login attempt limit
The original attempt-counter check (`if n>3`) ran *after* incrementing
inside the loop body in a way that allowed a 4th attempt before
denying access, despite the intent being 3 tries. Fixed to `n >= 3`,
checked immediately after incrementing.

### 5. Redundant/unused import
The original imported both `pymysql as mc` and, two lines later,
`mysql.connector as mc` — the second import silently overwrote the
first, making the `pymysql` import completely dead code (and an unused
dependency). Removed.

### 6. Games/arcade module removed entirely
Rock-Paper-Scissors, Tic-Tac-Toe, Hand Cricket, Hangman, and their
supporting helper functions and imports (`random as r`) have been
removed, along with the corresponding section of `help()` text and
command routing in `main.py`. This was contributed by teammates, not
part of my original authorship, and is out of scope for this review.

## Database migration: MySQL → SQLite

PandaVault is meant to be a *private, per-user vault* that each person
runs on their own device. MySQL is a server: it would force every user
to install and run MySQL, or make everyone share one hosted database —
both wrong for a private per-device vault. SQLite is embedded (Python's
stdlib `sqlite3`): zero-install, one local file per device, works
offline. So the record system was migrated from MySQL to SQLite.

- **Schema** (`schema.sql`): the original MySQL DDL was never in this
  repo (it lived on the external server), so the schema was
  reconstructed from how the code uses each table and written as SQLite
  DDL (`VARCHAR(n) → TEXT`, `INT → INTEGER`, money → `REAL`), with
  `PRIMARY KEY`s declared where the code deletes/edits/dedups by a
  column.
- **First-run bootstrap** (`init_db()` in `panda/vault.py`): creates
  `~/.pandavault/vault.db` and runs `schema.sql` on first launch, so the
  built-in tables exist as **empty** tables. Each user fills their own
  data, and can create their own tables at runtime.
- **Queries**: `%s` placeholders → `?`; `INSERT IGNORE` → `INSERT OR
  IGNORE`; `SHOW TABLES` → `sqlite_master`; `ALTER TABLE … ADD (…)` →
  `ALTER TABLE … ADD COLUMN`. The marksheet average was changed from
  `/5` to `/5.0` because SQLite does integer division on integers.
- **Config**: the MySQL host/user/password/database-name settings were
  removed (SQLite needs none); the weather/news API keys stay.

**Tables curated to what a personal vault actually needs.** Kept:
`Emergency` (medical info), `Medicine` (personal pharmacy log),
`Student_Marks` (exam marksheet). Removed as not fitting a private
per-user vault: `PANDA_Mart`, `Shopping_List`, `Transaction_History`
(a purchase log that could only be filled from the shopping list), and
`Panda_Counter` (a flight timetable).

## Project structure

```
panda-assistant/
├── main.py              # entry point — command loop and routing
├── config.py            # environment-based config (API keys, vault path)
├── schema.sql           # SQLite DDL for the built-in tables (run on first launch)
├── .env.example         # template for required environment variables
├── .gitignore
├── requirements.txt
├── DECISIONS.md         # decision record (MySQL→SQLite, table curation)
└── panda/
    ├── system.py         # help text, greeting, date/time/battery
    ├── auth.py           # password hashing and vault authentication
    ├── utilities.py       # reminders, jokes, news, weather, calculator, stopwatch, countdown, typing test
    └── vault.py          # PandaVault: the SQLite-backed record system + init_db()
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# fill in .env with your OpenWeatherMap and NewsAPI keys (no database setup needed)
python main.py
```

No database server or installation is required: on first run the app
creates a local SQLite vault at `~/.pandavault/vault.db` with the
built-in tables empty, ready for your own data.

## Known scope for further work

`panda/vault.py` is currently one large function (`DATABASE()`) with
nested sub-functions per table (Emergency, Medicine, Student_Marks) —
preserved as-is from the original implementation because it works
correctly and a large mechanical rewrite risked introducing bugs
without a matching benefit. A natural next step is converting this into
a proper class (e.g. `PandaVault`) with one method per table and the
connection passed in via `__init__` rather than relying on module-level
globals — but that's a distinct, larger refactor. Two other known
items, left out of the migration to keep it focused: the bare `except:`
blocks throughout `vault.py`, and the `.format()`-built SQL in the
free-form Search/Show/Creator functions (an injection risk for
user-supplied table/field names).
