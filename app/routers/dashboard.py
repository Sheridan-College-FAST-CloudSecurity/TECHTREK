# app/routers/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_patients = db.query(models.Patient).count()
    total_doctors = db.query(models.Doctor).count()
    upcoming_appointments = db.query(models.Appointment).filter(models.Appointment.status == "Scheduled").count()

    # Example: group patients by condition
    patients_by_department = {}
    for patient in db.query(models.Patient).all():
        dept = patient.condition
        patients_by_department[dept] = patients_by_department.get(dept, 0) + 1

    # Example: group appointments by status
    appointments_by_status = {}
    for appointment in db.query(models.Appointment).all():
        status = appointment.status
        appointments_by_status[status] = appointments_by_status.get(status, 0) + 1

    return schemas.DashboardSummary(
        total_patients=total_patients,
        total_doctors=total_doctors,
        upcoming_appointments=upcoming_appointments,
        appointments_by_status=appointments_by_status,
        patients_by_department=patients_by_department
    )
