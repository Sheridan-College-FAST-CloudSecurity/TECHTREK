from fastapi.testclient import TestClient
from app.main import app
import io
import datetime

client = TestClient(app)

def test_upload_lab_report():
    file_data = io.BytesIO(b"Sample test report")
    response = client.post("/labs/", files={"report": ("report.txt", file_data, "text/plain")},
        data={
            "patient_id": 1,
            "test_name": "Blood Test",
            "date_taken": str(datetime.date.today())
        })
    assert response.status_code == 200
    assert "report_file" in response.json()
