from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_department():
    response = client.post("/departments/", json={
        "name": "Cardiology", "description": "Heart-related dept"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Cardiology"

def test_get_departments():
    response = client.get("/departments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
