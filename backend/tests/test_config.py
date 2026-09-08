from pathlib import Path

import pytest
from app.config import Settings
from pydantic import ValidationError
from pytest import MonkeyPatch


def test_settings_use_environment_prefix(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("BETBOT_APP_ENV", "test")
    monkeypatch.setenv("BETBOT_APP_HOST", "0.0.0.0")
    monkeypatch.setenv("BETBOT_APP_PORT", "9000")
    monkeypatch.setenv("BETBOT_DEBUG", "true")
    monkeypatch.setenv(
        "BETBOT_DATABASE_URL",
        "postgresql+asyncpg://betbot:test@localhost:5432/test",
    )

    settings = Settings(_env_file=None)

    assert settings.app_env == "test"
    assert settings.app_host == "0.0.0.0"
    assert settings.app_port == 9000
    assert settings.debug is True


def test_settings_use_environment_database_url(monkeypatch: MonkeyPatch) -> None:
    database_url = "postgresql+asyncpg://betbot:test@localhost:5433/test"
    monkeypatch.setenv("BETBOT_DATABASE_URL", database_url)

    settings = Settings(_env_file=None)

    assert settings.database_url == database_url


def test_settings_load_environment_file_and_prefer_shell_values(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    environment_file = tmp_path / ".env"
    environment_file.write_text(
        "BETBOT_DATABASE_URL=postgresql+asyncpg://betbot:file@localhost:5432/file\n"
    )
    shell_database_url = "postgresql+asyncpg://betbot:shell@localhost:5432/shell"
    monkeypatch.setenv("BETBOT_DATABASE_URL", shell_database_url)

    settings = Settings(_env_file=environment_file)

    assert settings.database_url == shell_database_url


def test_settings_reject_missing_database_url(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("BETBOT_DATABASE_URL", raising=False)

    with pytest.raises(ValidationError, match="database_url"):
        Settings(_env_file=None)


def test_settings_reject_invalid_application_port(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv(
        "BETBOT_DATABASE_URL",
        "postgresql+asyncpg://betbot:test@localhost:5432/test",
    )
    monkeypatch.setenv("BETBOT_APP_PORT", "70000")

    with pytest.raises(ValidationError, match="app_port"):
        Settings(_env_file=None)


def test_settings_reject_blank_application_host(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv(
        "BETBOT_DATABASE_URL",
        "postgresql+asyncpg://betbot:test@localhost:5432/test",
    )
    monkeypatch.setenv("BETBOT_APP_HOST", "   ")

    with pytest.raises(ValidationError, match="app_host"):
        Settings(_env_file=None)


def test_settings_reject_invalid_database_url(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("BETBOT_DATABASE_URL", "not-a-database-url")

    with pytest.raises(ValidationError, match="postgresql\\+asyncpg"):
        Settings(_env_file=None)
