from pydantic import BaseModel
from datetime import date

class LabTestCreate(BaseModel):
    patient_id: int
    test_name: str
    date_taken: date

class LabTestOut(LabTestCreate):
    id: int
    report_file: str
