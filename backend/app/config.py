from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "BetBot API"
    environment: str = "development"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://localhost:5432/betbot"

    model_config = SettingsConfigDict(
        env_prefix="BETBOT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
