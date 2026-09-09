import os
from collections.abc import Iterator

import pytest
from app.config import Settings
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test"


def pytest_sessionstart() -> None:
    """Set safe defaults before application modules are collected."""
    os.environ.setdefault("BETBOT_APP_ENV", "test")
    os.environ.setdefault("BETBOT_APP_HOST", "127.0.0.1")
    os.environ.setdefault("BETBOT_APP_PORT", "8000")
    os.environ.setdefault("BETBOT_DEBUG", "false")
    os.environ.setdefault("BETBOT_DATABASE_URL", TEST_DATABASE_URL)


@pytest.fixture(autouse=True)
def test_environment(monkeypatch: MonkeyPatch) -> None:
    """Provide deterministic, non-production settings for every test."""
    monkeypatch.setenv("BETBOT_APP_ENV", "test")
    monkeypatch.setenv("BETBOT_APP_HOST", "127.0.0.1")
    monkeypatch.setenv("BETBOT_APP_PORT", "8000")
    monkeypatch.setenv("BETBOT_DEBUG", "false")
    monkeypatch.setenv("BETBOT_DATABASE_URL", TEST_DATABASE_URL)


@pytest.fixture
def test_settings() -> Settings:
    """Build settings without reading a developer or production .env file."""
    return Settings(
        _env_file=None,
        app_env="test",
        app_host="127.0.0.1",
        app_port=8000,
        debug=False,
        database_url=TEST_DATABASE_URL,
    )


@pytest.fixture
def test_client(test_settings: Settings) -> Iterator[TestClient]:
    """Create a client for the application configured for tests."""
    from app.main import create_app

    application: FastAPI = create_app(test_settings)
    with TestClient(application) as client:
        yield client
