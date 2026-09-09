import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_health_endpoint_is_available_through_integration_suite(
    test_client: TestClient,
) -> None:
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
