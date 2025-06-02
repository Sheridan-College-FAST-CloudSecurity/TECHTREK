from pydantic import BaseModel
from typing import Optional
from datetime import date

class Patient(BaseModel):
    id: Optional[int]
    name: str
    dob: date
    phone: str
    address: str

class Doctor(BaseModel):
    id: Optional[int]
    name: str
    specialty: str
    phone: str

class Appointment(BaseModel):
    id: Optional[int]
    patient_id: int
    doctor_id: int
    appointment_date: date
    status: Optional[str] = "Scheduled"

class Department(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None
