from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.schemas.patient_schema import Patient, PatientCreate  # ✅ Corrected import

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new patient
@router.post("/", response_model=Patient)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Retrieve all patients
@router.get("/", response_model=list[Patient])
def get_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()
