from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    user_role = Column(String, default="admin")  # or nurse, doctor
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
