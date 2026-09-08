from app.config import Settings
from pytest import MonkeyPatch


def test_settings_use_environment_prefix(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("BETBOT_ENVIRONMENT", "test")
    monkeypatch.setenv("BETBOT_DEBUG", "true")

    settings = Settings()

    assert settings.environment == "test"
    assert settings.debug is True


def test_settings_use_environment_database_url(monkeypatch: MonkeyPatch) -> None:
    database_url = "postgresql+asyncpg://user:password@localhost:5433/test"
    monkeypatch.setenv("BETBOT_DATABASE_URL", database_url)

    settings = Settings()

    assert settings.database_url == database_url
