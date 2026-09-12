"""
Central configuration for the Purchase Order app.

Loads settings from a .env file (see .env.example) so no credentials
are hard-coded in source, and exposes a helper for resolving asset
paths regardless of the current working directory.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# Load variables from a .env file at the project root, if present.
# Real deployments can also just set environment variables directly.
load_dotenv(BASE_DIR / ".env")


def asset_path(filename: str) -> str:
    """Return the absolute path to a file in the assets/ folder."""
    return str(ASSETS_DIR / filename)


def _required_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Copy .env.example to .env and fill in your MySQL credentials."
        )
    return value


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "purchase_order"),
}

APP_ICON = ASSETS_DIR / "icon.jpg"  # optional; app runs fine if missing
