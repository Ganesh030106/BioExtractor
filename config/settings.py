"""
Application Settings
--------------------
Centralised configuration loaded from environment variables / .env file.
All secrets (API keys, etc.) are read here and exposed as module-level constants.

Usage from anywhere in the project:
    from config.settings import GEMINI_API_KEY, GEMINI_MODEL
"""

import os
from dotenv import load_dotenv

# Load .env from the project root (one level above config/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENV_PATH = os.path.join(_PROJECT_ROOT, ".env")
load_dotenv(_ENV_PATH)

# ------------------------------------------------------------------ #
#  Google Gemini
# ------------------------------------------------------------------ #
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# ------------------------------------------------------------------ #
#  App Settings
# ------------------------------------------------------------------ #
APP_PORT = int(os.getenv("APP_PORT", "5000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"

# Quick validation helper
def is_gemini_configured():
    """Return True if a Gemini API key is present."""
    return bool(GEMINI_API_KEY and GEMINI_API_KEY.strip())
