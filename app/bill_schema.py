from pydantic import BaseModel
from datetime import date

class BillCreate(BaseModel):
    patient_id: int
    services: str  # like JSON or comma-separated
    total_amount: float

class BillOut(BillCreate):
    id: int
    date_issued: date
