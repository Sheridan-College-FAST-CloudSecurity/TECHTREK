from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.department_model import Department
from app.schemas.department_schema import DepartmentCreate, DepartmentOut
from app.database import get_db

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=DepartmentOut)
def create(dept: DepartmentCreate, db: Session = Depends(get_db)):
    new_dept = Department(**dept.dict())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@router.get("/", response_model=list[DepartmentOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(Department).all()
