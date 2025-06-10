import os
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.lab_model import LabTest
from app.schemas.lab_schema import LabTestOut

router = APIRouter(prefix="/labs", tags=["Lab"])

UPLOAD_DIR = "static/reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=LabTestOut)
async def upload_lab_test(
    patient_id: int = Form(...),
    test_name: str = Form(...),
    date_taken: date = Form(...),
    report: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{test_name}_{patient_id}_{report.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(await report.read())

    new_test = LabTest(
        patient_id=patient_id,
        test_name=test_name,
        date_taken=date_taken,
        report_file=filepath
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test

@router.get("/by_patient/{patient_id}", response_model=list[LabTestOut])
def get_patient_tests(patient_id: int, db: Session = Depends(get_db)):
    return db.query(LabTest).filter(LabTest.patient_id == patient_id).all()
