from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: datetime

appointments_db = []

@router.get("/", response_model=List[Appointment])
def get_appointments():
    return appointments_db

@router.get("/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: int):
    for app in appointments_db:
        if app.id == appointment_id:
            return app
    raise HTTPException(status_code=404, detail="Appointment not found")

@router.post("/", response_model=Appointment)
def create_appointment(appointment: Appointment):
    appointments_db.append(appointment)
    return appointment

@router.put("/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: int, updated: Appointment):
    for i, app in enumerate(appointments_db):
        if app.id == appointment_id:
            appointments_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Appointment not found")

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int):
    for i, app in enumerate(appointments_db):
        if app.id == appointment_id:
            del appointments_db[i]
            return {"detail": "Appointment deleted"}
    raise HTTPException(status_code=404, detail="Appointment not found")
