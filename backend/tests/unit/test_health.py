from typing import cast

import pytest
from app.config import Settings
from app.infrastructure.database import DatabaseReadiness
from app.main import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit


class AvailableDatabase:
    async def is_available(self) -> bool:
        return True

    async def dispose(self) -> None:
        return None


class UnavailableDatabase:
    async def is_available(self) -> bool:
        return False

    async def dispose(self) -> None:
        return None


class DisposableDatabase(AvailableDatabase):
    def __init__(self) -> None:
        self.disposed = False

    async def dispose(self) -> None:
        self.disposed = True


def replace_database(test_client: TestClient, database: DatabaseReadiness) -> None:
    """Replace the app-owned database with a deterministic test double."""
    application = cast(FastAPI, test_client.app)
    application.state.database = database


def test_health_endpoint_reports_running_application(test_client: TestClient) -> None:
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_does_not_require_database(test_client: TestClient) -> None:
    replace_database(test_client, UnavailableDatabase())

    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_endpoint_reports_available_database(test_client: TestClient) -> None:
    replace_database(test_client, AvailableDatabase())

    response = test_client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_readiness_endpoint_reports_unavailable_database(
    test_client: TestClient,
) -> None:
    replace_database(test_client, UnavailableDatabase())

    response = test_client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "database": "unavailable"}


def test_application_uses_configured_debug_mode() -> None:
    settings = Settings(
        database_url="postgresql+asyncpg://betbot:test@localhost:5432/test",
        debug=True,
    )

    application = create_app(settings)

    assert application.debug is True


def test_application_disposes_database_at_shutdown(test_settings: Settings) -> None:
    application = create_app(test_settings)
    database = DisposableDatabase()
    application.state.database = database

    with TestClient(application):
        pass

    assert database.disposed is True
