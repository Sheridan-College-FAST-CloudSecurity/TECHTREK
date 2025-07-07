from fastapi import APIRouter
from app.schemas.dashboard_schema import DashboardSummary

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    return {
        "total_patients": 100,
        "total_doctors": 20,
        "upcoming_appointments": 10,
        "appointments_by_status": {
            "scheduled": 6,
            "completed": 3,
            "cancelled": 1
        },
        "patients_by_department": {
            "cardiology": 50,
            "neurology": 30,
            "orthopedics": 20
        }
    }

