from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    id: int
    name: str
    age: Optional[int] = None

class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
