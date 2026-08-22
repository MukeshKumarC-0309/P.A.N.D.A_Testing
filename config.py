"""
Configuration and secrets loading.

All credentials are read from environment variables instead of being
hardcoded in source. Create a `.env` file (see .env.example) or export
these variables in your shell before running the assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables, if present


# PandaVault is an embedded SQLite database: no host/user/password/database
# name is needed. The vault is a single local file, one per device, kept in
# the user's home directory so it survives regardless of the launch directory.
# Override with PANDA_DB_PATH (handy for tests or a custom location).
DEFAULT_DB_PATH = Path.home() / ".pandavault" / "vault.db"
DB_PATH = Path(os.environ.get("PANDA_DB_PATH", DEFAULT_DB_PATH))

WEATHER_API_KEY = os.environ.get("PANDA_WEATHER_API_KEY")
NEWS_API_KEY = os.environ.get("PANDA_NEWS_API_KEY")

if WEATHER_API_KEY is None:
    raise RuntimeError(
        "PANDA_WEATHER_API_KEY is not set. Create a .env file (see .env.example) "
        "or export PANDA_WEATHER_API_KEY in your shell before running PANDA."
    )

if NEWS_API_KEY is None:
    raise RuntimeError(
        "PANDA_NEWS_API_KEY is not set. Create a .env file (see .env.example) "
        "or export PANDA_NEWS_API_KEY in your shell before running PANDA."
    )
