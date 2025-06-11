from sqlalchemy import Column, Integer, String
from app.database import Base

class Nurse(Base):
    __tablename__ = "nurses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String)
    phone = Column(String)
    shift = Column(String)
