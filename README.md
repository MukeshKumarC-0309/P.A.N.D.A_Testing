# P.A.N.D.A — Security Review & Restructure

A revisit of a 12th-grade school project: a Python CLI assistant with a
MySQL-backed record management system ("PandaVault"). This version
removes the games/arcade module and fixes several real security and
correctness issues found during review, using skills developed since
the original was built.

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

## Project structure

```
panda-assistant/
├── main.py              # entry point — command loop and routing
├── config.py            # environment-based secrets loading
├── .env.example         # template for required environment variables
├── .gitignore
├── requirements.txt
└── panda/
    ├── system.py         # help text, greeting, date/time/battery
    ├── auth.py           # password hashing and vault authentication
    ├── utilities.py       # reminders, jokes, news, weather, calculator, stopwatch, countdown, typing test
    └── vault.py          # PandaVault: the database-backed record system
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# fill in .env with your own MySQL credentials and API keys
python main.py
```

## Known scope for further work

`panda/vault.py` is currently one large function (`DATABASE()`) with
~30 nested sub-functions, one per table (Emergency records, Medicine,
Marksheet, Shopping List, etc.) — preserved as-is from the original
implementation because it works correctly and a large mechanical
rewrite risked introducing bugs without a matching benefit. A natural
next step is converting this into a proper class (e.g. `PandaVault`)
with one method per table and a connection passed in via `__init__`
rather than relying on module-level globals — but that's a distinct,
larger refactor from this security-focused pass.
