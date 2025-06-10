from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    message: str
    user_role: str = "admin"

class NotificationOut(NotificationCreate):
    id: int
    created_at: datetime
    is_read: bool
