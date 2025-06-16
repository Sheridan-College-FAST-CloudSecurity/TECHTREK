import logging
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
from src.services.db import DatabaseManagement
from src.common.models import Staff, StaffOut
from fastapi import HTTPException

app = FastAPI()

origins = [
    "https://solid-fortnight-694rjj4gw67qc4rgq-8080.app.github.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = DatabaseManagement()

# Logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler - to log to a file
file_handler = logging.FileHandler("api.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Add handlers to the logger
logger.addHandler(file_handler)


# Root endpoint
@app.get("/")
def root():
    logger.info("Request: GET /")
    return {"message": "Welcome to the PyPharma API"}

  
# Health check endpoint
@app.get("/health")
def health_check():
    logger.info("Request: GET /health")
    return {"status": "ok"}

# Table check endpoint
@app.get("/table")
def create_table():
    logger.info("Request: GET /create tables/")
    return db.create_table()

# admin login
def admin_login():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    conn.commit()
    conn.close()
create_table()
admin_login()

#login API
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    logger.info(username, "Testing")
    conn.close()
    if result:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)

# Add Doctor (insert staff with role="doctor")
@app.post("/doctors", response_model=StaffOut)
def add_doctor(doctor: Staff):
    if doctor.role.lower() != "doctor":
        raise HTTPException(status_code=400, detail="Role must be 'doctor'")
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Staff (name, contact_number, role, dept, email)
        VALUES (?, ?, ?, ?, ?)
    """, (doctor.name, doctor.contact_number, doctor.role, doctor.dept, doctor.email))
    conn.commit()
    doctor_id = cursor.lastrowid
    conn.close()
    return {**doctor.dict(), "id": doctor_id}

# Get All Doctors
@app.get("/doctors", response_model=list[StaffOut])
def get_doctors():
    logger.info("Testing for load doctors")
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff WHERE role = 'Doctor'")
    rows = cursor.fetchall()
    conn.close()
    return [
            {
                **dict(row),
                "contact_number": str(row["contact_number"])
            }
            for row in rows
        ]
# Get Single Doctor
@app.get("/doctors/{doctor_id}", response_model=StaffOut)
def get_doctor(doctor_id: int):
    logger.info("Edit doctor information")
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff WHERE id=? AND role='Doctor'", (doctor_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor = dict(row)
    doctor["contact_number"] = str(doctor["contact_number"])
    return doctor

# Update Doctor
@app.put("/doctors/{doctor_id}", response_model=StaffOut)
def update_doctor(doctor_id: int, doctor: Staff):
    logger.info("Testing for edit")
    if doctor.role.lower() != "doctor":
        raise HTTPException(status_code=400, detail="Role must be 'doctor'")
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff WHERE id=? AND role='Doctor'", (doctor_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    cursor.execute("""
        UPDATE Staff SET name=?, contact_number=?, role=?, dept=?, email=?
        WHERE id=?
    """, (doctor.name, doctor.contact_number, doctor.role, doctor.dept, doctor.email, doctor_id))
    conn.commit()
    conn.close()
    return {**doctor.dict(), "id": doctor_id}

# Delete Doctor
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM staff WHERE id=? AND role='Doctor'", (doctor_id,))
    conn.commit()
    conn.close()
    return {"message": f"Doctor with ID {doctor_id} deleted"}