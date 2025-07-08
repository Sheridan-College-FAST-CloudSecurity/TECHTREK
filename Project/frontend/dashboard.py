from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Patient, Doctor, Appointment
from schemas import DashboardSummary
from datetime import datetime

router = APIRouter()

@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_patients = db.query(Patient).count()
    total_doctors = db.query(Doctor).count()
    upcoming_appointments = db.query(Appointment).filter(Appointment.datetime >= datetime.now()).count()

    # Group appointments by status
    appointments_status_counts = (
        db.query(Appointment.status, func.count(Appointment.id))
        .group_by(Appointment.status)
        .all()
    )
    appointments_by_status = {status: count for status, count in appointments_status_counts}

    # Group patients by department
    patients_dept_counts = (
        db.query(Patient.department, func.count(Patient.id))
        .group_by(Patient.department)
        .all()
    )
    patients_by_department = {dept: count for dept, count in patients_dept_counts}

    return DashboardSummary(
        total_patients=total_patients,
        total_doctors=total_doctors,
        upcoming_appointments=upcoming_appointments,
        appointments_by_status=appointments_by_status,
        patients_by_department=patients_by_department,
    )
