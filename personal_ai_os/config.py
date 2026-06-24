"""Application configuration loaded from environment variables and .env files."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - used when optional deps are not installed yet
    def load_dotenv(dotenv_path=None):
        return False


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the Personal AI OS."""

    openai_api_key: str | None
    openai_model: str
    database_path: Path
    log_level: str
    workspace_path: Path
    max_tool_rounds: int
    search_provider: str


def load_settings(env_file: str | Path | None = None) -> Settings:
    """Load settings from .env and process environment variables."""
    load_dotenv(dotenv_path=env_file)
    workspace = Path(os.getenv("PAI_WORKSPACE", ".")).expanduser().resolve()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        database_path=Path(os.getenv("PAI_DB_PATH", ".personal_ai_os/memory.sqlite3")).expanduser(),
        log_level=os.getenv("PAI_LOG_LEVEL", "INFO"),
        workspace_path=workspace,
        max_tool_rounds=int(os.getenv("PAI_MAX_TOOL_ROUNDS", "6")),
        search_provider=os.getenv("PAI_SEARCH_PROVIDER", "duckduckgo"),
    )
