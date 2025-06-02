from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Patient(BaseModel):
    id: int
    name: str
    age: int

patients_db = []

@router.get("/", response_model=List[Patient])
def get_patients():
    return patients_db

@router.get("/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    for patient in patients_db:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@router.post("/", response_model=Patient)
def create_patient(patient: Patient):
    patients_db.append(patient)
    return patient

@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, updated: Patient):
    for i, pat in enumerate(patients_db):
        if pat.id == patient_id:
            patients_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Patient not found")

@router.delete("/{patient_id}")
def delete_patient(patient_id: int):
    for i, pat in enumerate(patients_db):
        if pat.id == patient_id:
            del patients_db[i]
            return {"detail": "Patient deleted"}
    raise HTTPException(status_code=404, detail="Patient not found")
