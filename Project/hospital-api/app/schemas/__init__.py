# app/schemas/dashboard_schema.py
from pydantic import BaseModel
# app/schemas/__init__.py

from .dashboard_schema import DashboardSummary

class DashboardSummary(BaseModel):
    total_patients: int
    total_doctors: int
    total_appointments: int
