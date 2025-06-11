from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import patients, doctors, appointments, dashboard, departments  # 👈 include dashboard

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve dashboard.html directly
@app.get("/", response_class=FileResponse)
def dashboard_page():
    return "static/dashboard.html"

# Include your routers
from app.routers import dashboard
app.include_router(dashboard.router)

from app.routers import departments
app.include_router(departments.router)

from app.routers import nurses
app.include_router(nurses.router)

from app.routers import medicines
app.include_router(medicines.router)

from app.routers import labs
app.include_router(labs.router)

from app.routers import billing
app.include_router(billing.router)

from app.routers import notifications
app.include_router(notifications.router)

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

models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])  # ✅ this line
