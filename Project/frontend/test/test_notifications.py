from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_notification():
    res = client.post("/notifications/", json={"message": "Test Alert", "user_role": "admin"})
    assert res.status_code == 200
    assert res.json()["message"] == "Test Alert"

def test_get_unread():
    res = client.get("/notifications/unread/admin")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_mark_as_read():
    # Mark the first unread as read
    unread = client.get("/notifications/unread/admin").json()
    if unread:
        id = unread[0]["id"]
        res = client.post(f"/notifications/mark_read/{id}")
        assert res.status_code == 200
