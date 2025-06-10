from fastapi import APIRouter, Query

router = APIRouter()

appointments_data = [
    {"id": 1, "patient_id": 1, "date": "2025-06-09", "doctor": "Dr. Smith"},
    {"id": 2, "patient_id": 2, "date": "2025-06-10", "doctor": "Dr. Jones"},
]

@router.get("/")
def get_appointments(patient_id: int = Query(..., description="Patient ID"), date: str = Query(..., description="Appointment date YYYY-MM-DD")):
    filtered = [appt for appt in appointments_data if appt["patient_id"] == patient_id and appt["date"] == date]
    return filtered
