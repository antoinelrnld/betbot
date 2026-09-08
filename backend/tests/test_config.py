from app.config import Settings
from pytest import MonkeyPatch


def test_settings_use_environment_prefix(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("BETBOT_ENVIRONMENT", "test")
    monkeypatch.setenv("BETBOT_DEBUG", "true")

    settings = Settings()

    assert settings.environment == "test"
    assert settings.debug is True
