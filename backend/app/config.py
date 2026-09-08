from functools import lru_cache
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

BACKEND_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "BetBot API"
    app_env: Literal["development", "test", "production"] = "development"
    app_host: str = Field(default="127.0.0.1", min_length=1)
    app_port: int = Field(default=8000, ge=1, le=65535)
    debug: bool = False
    database_url: str = Field(min_length=1)

    model_config = SettingsConfigDict(
        env_prefix="BETBOT_",
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("app_host")
    @classmethod
    def validate_app_host(cls, value: str) -> str:
        """Reject empty bind addresses before starting the server."""
        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError("must not be blank")
        return normalized_value

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        """Require a complete async PostgreSQL connection URL."""
        try:
            database_url = make_url(value)
        except ArgumentError as error:
            raise ValueError(
                "must be a valid postgresql+asyncpg connection URL"
            ) from error

        if (
            database_url.drivername != "postgresql+asyncpg"
            or database_url.host is None
            or database_url.database is None
        ):
            raise ValueError("must be a complete postgresql+asyncpg connection URL")

        return value

    @model_validator(mode="after")
    def validate_debug_mode(self) -> Self:
        """Prevent verbose exception responses in production."""
        if self.app_env == "production" and self.debug:
            raise ValueError("debug mode cannot be enabled in production")
        return self


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings()
