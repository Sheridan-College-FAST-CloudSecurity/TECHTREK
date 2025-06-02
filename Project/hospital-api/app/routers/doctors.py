from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter()

class Doctor(BaseModel):
    id: int
    name: str
    specialty: str
    email: EmailStr
    phone: str
    years_experience: int
    available: bool

class DoctorCreate(BaseModel):
    # No ID here, will be generated automatically
    name: str
    specialty: str
    email: EmailStr
    phone: str
    years_experience: int
    available: bool

class DoctorUpdate(BaseModel):
    # All fields optional for PATCH updates
    name: Optional[str]
    specialty: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    years_experience: Optional[int]
    available: Optional[bool]

doctors = [
    {
        "id": 1,
        "name": "Dr. Smith",
        "specialty": "Cardiology",
        "email": "smith@example.com",
        "phone": "555-1234",
        "years_experience": 15,
        "available": True
    },
    {
        "id": 2,
        "name": "Dr. Jones",
        "specialty": "Neurology",
        "email": "jones@example.com",
        "phone": "555-5678",
        "years_experience": 10,
        "available": False
    },
]

@router.get("/", response_model=List[Doctor])
async def get_doctors():
    return doctors

@router.get("/count")
async def get_doctors_count():
    return {"total_doctors": len(doctors)}

@router.get("/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: int):
    for doc in doctors:
        if doc["id"] == doctor_id:
            return doc
    raise HTTPException(status_code=404, detail="Doctor not found")

@router.post("/", response_model=Doctor, status_code=201)
async def create_doctor(doctor: DoctorCreate):
    max_id = max((d["id"] for d in doctors), default=0)
    new_doctor = doctor.dict()
    new_doctor["id"] = max_id + 1
    doctors.append(new_doctor)
    return new_doctor

@router.put("/{doctor_id}", response_model=Doctor)
async def update_doctor(doctor_id: int, doctor: DoctorCreate):
    for index, doc in enumerate(doctors):
        if doc["id"] == doctor_id:
            updated_doctor = doctor.dict()
            updated_doctor["id"] = doctor_id  # keep the same id
            doctors[index] = updated_doctor
            return updated_doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@router.patch("/{doctor_id}", response_model=Doctor)
async def partial_update_doctor(doctor_id: int, doctor_update: DoctorUpdate):
    for index, doc in enumerate(doctors):
        if doc["id"] == doctor_id:
            updated_data = doc.copy()
            update_fields = doctor_update.dict(exclude_unset=True)
            updated_data.update(update_fields)
            doctors[index] = updated_data
            return updated_data
    raise HTTPException(status_code=404, detail="Doctor not found")

@router.delete("/{doctor_id}", status_code=204)
async def delete_doctor(doctor_id: int):
    for index, doc in enumerate(doctors):
        if doc["id"] == doctor_id:
            doctors.pop(index)
            return
    raise HTTPException(status_code=404, detail="Doctor not found")
