import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Hospital Patients</title>" in response.text or "<title>Patients</title>" in response.text

def test_patients_endpoint():
    response = client.get("/patients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_doctors_endpoint():
    response = client.get("/doctors/", params={"available": "true"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(doc["available"] is True for doc in data)

def test_departments_endpoint():
    response = client.get("/departments/", params={"hospital_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("name" in dept for dept in data)

def test_appointments_endpoint():
    response = client.get("/appointments/", params={"patient_id": 1, "date": "2025-06-09"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(appt["patient_id"] == 1 and appt["date"] == "2025-06-09" for appt in data)

def test_create_patient():
    new_patient = {
        "id": 123,
        "name": "John Doe",
        "age": 30,
        "condition": "Healthy"
    }
    response = client.post("/patients/", json=new_patient)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 123
    assert data["name"] == "John Doe"
