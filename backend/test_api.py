import requests

Base_URL = "http://127.0.0.1:8000/"

def test_get_customers():
    res = requests.get(f"{Base_URL}/customers")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_add_customer():
    payload = {"id": 5, "name": "ps", "contact_number": "455566666", "email": "p@gmail.com",
                "DOB": "2025-04-16",
                "gender": "female",
                "address": "canada",
                "prescription_id": 2343456
                }
    res = requests.post(f"{Base_URL}/customers", json=payload)
    assert res.status_code == 200
    