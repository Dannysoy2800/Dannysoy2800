"""Centralized application configuration loaded from environment variables and .env files."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - used before optional dependencies are installed
    def load_dotenv(dotenv_path=None):
        return False


@dataclass(frozen=True)
class Settings:
    """Runtime settings for Personal AI OS v2."""

    openai_api_key: str | None
    openai_model: str
    database_path: Path
    log_level: str
    max_tool_rounds: int

    def require_openai_api_key(self) -> str:
        """Return the OpenAI API key or raise a clear configuration error."""
        if not self.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required for `ask` and `chat` commands.")
        return self.openai_api_key


def load_settings(env_file: str | Path | None = None) -> Settings:
    """Load settings from .env and process environment variables."""
    load_dotenv(dotenv_path=env_file)
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        database_path=Path(os.getenv("PAI_DB_PATH", ".personal_ai_os/conversations.sqlite3")).expanduser(),
        log_level=os.getenv("PAI_LOG_LEVEL", "INFO"),
        max_tool_rounds=int(os.getenv("PAI_MAX_TOOL_ROUNDS", "6")),
    )
