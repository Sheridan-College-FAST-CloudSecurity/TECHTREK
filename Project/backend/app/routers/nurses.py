from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.nurse_model import Nurse
from app.schemas.nurse_schema import NurseCreate, NurseOut
from app.database import get_db

router = APIRouter(prefix="/nurses", tags=["Nurses"])

@router.post("/", response_model=NurseOut)
def create_nurse(nurse: NurseCreate, db: Session = Depends(get_db)):
    new_nurse = Nurse(**nurse.dict())
    db.add(new_nurse)
    db.commit()
    db.refresh(new_nurse)
    return new_nurse

@router.get("/", response_model=list[NurseOut])
def get_all_nurses(db: Session = Depends(get_db)):
    return db.query(Nurse).all()

@router.delete("/{nurse_id}")
def delete_nurse(nurse_id: int, db: Session = Depends(get_db)):
    nurse = db.query(Nurse).get(nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found")
    db.delete(nurse)
    db.commit()
    return {"message": "Deleted successfully"}
