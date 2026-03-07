from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from pyflow_ai_stack.services.health_service import HealthService


def get_health_service():
    return HealthService(app_name="test-integration-app")


app = FastAPI()


@app.get("/health")
async def health_check(
    depends: int = 0, service: HealthService = Depends(get_health_service)
):
    return await service.check_health(depends=depends)


client = TestClient(app)


def test_integration_health_check_basic():
    """Test the health check integration with a FastAPI app."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "test-integration-app"


def test_integration_health_check_full():
    """Test the health check integration with dependencies."""
    # This will use the default (None) services in the HealthService
    response = client.get("/health?depends=1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    # Since we didn't provide services to HealthService, it won't have redis/gemini/s3 keys
    # unless we mock get_health_service to return a version with mocks.
    # But for a basic integration test of the endpoint itself, this is fine.
    assert "redis" not in data
