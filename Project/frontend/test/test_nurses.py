from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_nurse():
    response = client.post("/nurses/", json={
        "name": "Nina", "role": "ICU", "phone": "123456", "shift": "Night"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Nina"

def test_get_nurses():
    response = client.get("/nurses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
