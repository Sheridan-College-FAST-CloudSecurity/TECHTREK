from fastapi.testclient import TestClient
from app.main import app
import datetime

client = TestClient(app)

def test_add_medicine():
    response = client.post("/medicines/", json={
        "name": "Paracetamol",
        "batch": "P123",
        "expiry_date": str(datetime.date.today().replace(year=2026)),
        "stock": 100
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Paracetamol"

def test_get_meds():
    response = client.get("/medicines/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_expired_meds():
    response = client.get("/medicines/expired")
    assert response.status_code == 200
