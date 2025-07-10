from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notification_model import Notification
from app.schemas.notification_schema import NotificationCreate, NotificationOut

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationOut)
def create_notification(n: NotificationCreate, db: Session = Depends(get_db)):
    new = Notification(**n.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.get("/unread/{role}", response_model=list[NotificationOut])
def get_unread(role: str, db: Session = Depends(get_db)):
    return db.query(Notification).filter_by(user_role=role, is_read=False).all()

@router.post("/mark_read/{notif_id}")
def mark_as_read(notif_id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter_by(id=notif_id).first()
    if notif:
        notif.is_read = True
        db.commit()
        return {"status": "marked as read"}
    return {"error": "Notification not found"}
