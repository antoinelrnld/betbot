import pytest
from app.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit


def test_health_endpoint_reports_running_application(test_client: TestClient) -> None:
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_application_uses_configured_debug_mode() -> None:
    settings = Settings(
        database_url="postgresql+asyncpg://betbot:test@localhost:5432/test",
        debug=True,
    )

    application = create_app(settings)

    assert application.debug is True
