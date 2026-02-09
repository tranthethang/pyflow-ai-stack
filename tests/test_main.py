import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)


def test_health_check_basic():
    """Test the basic health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == get_settings().APP_NAME
    assert "redis" not in data
    assert "gemini" not in data
    assert "s3" not in data


def test_health_check_full():
    """Test the health check endpoint with dependencies."""
    # We don't necessarily need to mock services here if we just want to check the structure,
    # but the endpoint calls ping() on services.
    # For a simple integration-style check, we can just hit it.
    response = client.get("/health?depends=1")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "app" in data
    assert "redis" in data
    assert "gemini" in data
    assert "s3" in data
