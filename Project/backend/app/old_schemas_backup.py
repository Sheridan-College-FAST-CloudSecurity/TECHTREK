from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

# -------------------- Patient Schema --------------------
class PatientBase(BaseModel):
    name: str
    age: int
    condition: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True

# -------------------- Doctor Schema --------------------
class DoctorBase(BaseModel):
    name: str
    specialty: str

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True

# -------------------- Appointment Schema --------------------
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: datetime
    status: Optional[str] = "Scheduled"

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True

# -------------------- Dashboard Summary --------------------
class DashboardSummary(BaseModel):
    total_patients: int
    total_doctors: int
    upcoming_appointments: int
    appointments_by_status: Dict[str, int]
    patients_by_department: Dict[str, int]
