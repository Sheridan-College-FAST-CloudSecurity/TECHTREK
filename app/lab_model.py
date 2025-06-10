from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base

class LabTest(Base):
    __tablename__ = "lab_tests"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    test_name = Column(String, nullable=False)
    report_file = Column(String)  # path to file
    date_taken = Column(Date)
