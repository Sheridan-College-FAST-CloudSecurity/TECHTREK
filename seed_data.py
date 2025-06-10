from app.database import SessionLocal
from app import models

db = SessionLocal()

# Add doctors
doctor1 = models.Doctor(name="Dr. Smith", specialty="Cardiology", available=True)
doctor2 = models.Doctor(name="Dr. Lee", specialty="Dermatology", available=False)

# Add patients
patient1 = models.Patient(name="Alice", age=30, condition="Cardiology")
patient2 = models.Patient(name="Bob", age=45, condition="Dermatology")

# Add appointments
from datetime import datetime, timedelta

appointment1 = models.Appointment(
    patient=patient1,
    doctor=doctor1,
    datetime=datetime.now() + timedelta(days=1),
    reason="Check-up",
    status="Scheduled"
)

appointment2 = models.Appointment(
    patient=patient2,
    doctor=doctor2,
    datetime=datetime.now() + timedelta(days=2),
    reason="Skin rash",
    status="Scheduled"
)

db.add_all([doctor1, doctor2, patient1, patient2, appointment1, appointment2])
db.commit()
db.close()

print("✅ Seed data inserted!")
