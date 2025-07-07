# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models
from app.routers import (
    patients, doctors, appointments, dashboard, departments,
    nurses, medicine, labs, billing, notifications
)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve dashboard.html
@app.get("/", response_class=FileResponse)
def dashboard_page():
    return FileResponse("static/dashboard.html")

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(departments.router, prefix="/departments", tags=["Departments"])
app.include_router(nurses.router, prefix="/nurses", tags=["Nurses"])
app.include_router(medicines.router, prefix="/medicine", tags=["Medicines"])
app.include_router(labs.router, prefix="/labs", tags=["Labs"])
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
