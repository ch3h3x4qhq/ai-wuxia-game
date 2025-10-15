from fastapi.testclient import TestClient

from app.main import app


def test_health_ok() -> None:
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "ts" in data
