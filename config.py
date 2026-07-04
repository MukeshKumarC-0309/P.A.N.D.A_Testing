"""
Configuration and secrets loading.

All credentials are read from environment variables instead of being
hardcoded in source. Create a `.env` file (see .env.example) or export
these variables in your shell before running the assistant.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables, if present


DB_HOST = os.environ.get("PANDA_DB_HOST", "localhost")
DB_USER = os.environ.get("PANDA_DB_USER", "root")
DB_PASSWORD = os.environ.get("PANDA_DB_PASSWORD")
DB_NAME = os.environ.get("PANDA_DB_NAME", "project_Vedha")

WEATHER_API_KEY = os.environ.get("PANDA_WEATHER_API_KEY")
NEWS_API_KEY = os.environ.get("PANDA_NEWS_API_KEY")

if DB_PASSWORD is None:
    raise RuntimeError(
        "PANDA_DB_PASSWORD is not set. Create a .env file (see .env.example) "
        "or export PANDA_DB_PASSWORD in your shell before running PANDA."
    )

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
