from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    batch = Column(String)
    expiry_date = Column(Date)
    stock = Column(Integer)
