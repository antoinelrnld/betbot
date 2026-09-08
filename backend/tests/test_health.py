from app.main import create_app
from fastapi.testclient import TestClient


def test_health_endpoint_reports_running_application() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
