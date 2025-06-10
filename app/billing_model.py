from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text
from app.database import Base
import datetime

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    services = Column(Text)  # comma-separated or JSON
    total_amount = Column(Float)
    date_issued = Column(Date, default=datetime.date.today)
