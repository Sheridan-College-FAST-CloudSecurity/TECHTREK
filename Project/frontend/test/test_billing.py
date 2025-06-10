from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_bill():
    response = client.post("/billing/", json={
        "patient_id": 1,
        "services": "Consultation, MRI",
        "total_amount": 350.00
    })
    assert response.status_code == 200
    assert response.json()["total_amount"] == 350.00

def test_get_bills():
    response = client.get("/billing/by_patient/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
