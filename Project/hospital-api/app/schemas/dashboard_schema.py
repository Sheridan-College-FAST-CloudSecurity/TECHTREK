# app/schemas/dashboard_schema.py

from pydantic import BaseModel
from typing import Dict

class DashboardSummary(BaseModel):
    total_patients: int
    total_doctors: int
    upcoming_appointments: int
    appointments_by_status: Dict[str, int]
    patients_by_department: Dict[str, int]
