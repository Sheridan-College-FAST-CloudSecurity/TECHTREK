from pydantic import BaseModel
from datetime import date

class MedicineCreate(BaseModel):
    name: str
    batch: str
    expiry_date: date
    stock: int

class MedicineOut(MedicineCreate):
    id: int
