"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the OmniRouter AI API."""

    app_name: str = "OmniRouter AI"
    environment: str = "development"
    log_level: str = "INFO"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"

    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"

    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_site_url: str | None = None
    openrouter_app_name: str = "OmniRouter AI"

    provider_order: list[str] = Field(
        default_factory=lambda: ["gemini", "groq", "openrouter"]
    )
    request_timeout_seconds: float = 30.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="OMNI_",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings for dependency injection."""

    return Settings()
