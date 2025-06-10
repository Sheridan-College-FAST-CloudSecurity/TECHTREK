from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.models.medicine_model import Medicine
from app.schemas.medicine_schema import MedicineCreate, MedicineOut
from app.database import get_db

router = APIRouter(prefix="/medicines", tags=["Pharmacy"])

@router.post("/", response_model=MedicineOut)
def add_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    new_medicine = Medicine(**medicine.dict())
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine

@router.get("/", response_model=list[MedicineOut])
def list_medicines(db: Session = Depends(get_db)):
    return db.query(Medicine).all()

@router.put("/{medicine_id}")
def update_stock(medicine_id: int, stock: int, db: Session = Depends(get_db)):
    med = db.query(Medicine).get(medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    med.stock = stock
    db.commit()
    return {"message": "Stock updated"}

@router.get("/expired")
def expired_meds(db: Session = Depends(get_db)):
    today = date.today()
    expired = db.query(Medicine).filter(Medicine.expiry_date < today).all()
    return expired
