from fastapi import FastAPI
from app.routers import doctors, patients, appointments, departments

app = FastAPI()

app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(departments.router, prefix="/departments", tags=["Departments"])
