from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.billing_model import Bill
from app.schemas.bill_schema import BillCreate, BillOut

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/", response_model=BillOut)
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    new_bill = Bill(**bill.dict())
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill

@router.get("/by_patient/{patient_id}", response_model=list[BillOut])
def get_bills(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Bill).filter(Bill.patient_id == patient_id).all()
