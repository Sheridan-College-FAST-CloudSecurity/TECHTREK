import logging
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
from src.services.db import DatabaseManagement
from src.common.models import Staff, StaffOut, Customer, PatientOut, AppointmentOut, AppointmentCreate, Medicine, MedicineOut, PrescriptionItem, PrescriptionCreate, PrescriptionOut
from fastapi import HTTPException
from typing import List

app = FastAPI()

origins = [
    "http://54.88.179.164:8001"
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
    # logger.info(username, "Testing")
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
@app.get("/doctors", response_model=List[StaffOut])
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

# Create Patient
@app.post("/patients", response_model=PatientOut)
def add_patient(patient: Customer):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO customers (name, contact_number, email, DOB, gender, address, prescription_id, condition, staff_id, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient.name,
        patient.contact_number,
        patient.email,
        patient.DOB,
        patient.gender,
        patient.address,
        patient.prescription_id,
        patient.condition,
        patient. staff_id,
        patient. status
    ))
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    return {**patient.dict(), "id": patient_id}

# Read All Patients
@app.get("/patients", response_model=List[PatientOut])
def get_patients():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            **dict(row),
            "contact_number": str(row["contact_number"]),
            "prescription_id": row["prescription_id"] if row["prescription_id"] is not None else None
        }
        for row in rows
    ]

# Read One Patient
@app.get("/patients/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = dict(row)
    patient["contact_number"] = str(patient["contact_number"])
    patient["prescription_id"] = row["prescription_id"] if row["prescription_id"] is not None else None
    return patient

# Update Patient
@app.put("/patients/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, patient: Customer):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id=?", (patient_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")

    cursor.execute("""
        UPDATE customers SET name=?, contact_number=?, email=?, DOB=?, gender=?, address=?, prescription_id=?
        WHERE id=?
    """, (
        patient.name,
        patient.contact_number,
        patient.email,
        patient.DOB,
        patient.gender,
        patient.address,
        patient.prescription_id,
        patient_id
    ))
    conn.commit()
    conn.close()
    return {**patient.dict(), "id": patient_id}
    
# Delete Patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()
    return {"message": f"Patient with ID {patient_id} deleted"}

# Create Appointment
@app.post("/appointments", response_model=AppointmentOut)
def add_appointment(appointment: AppointmentCreate):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_name, age, condition, doctor_name)
        VALUES (?, ?, ?, ?)
    """, (
        appointment.patient_name,
        appointment.age,
        appointment.condition,
        appointment.doctor_name
    ))
    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()
    return {**appointment.dict(), "id": appointment_id}

# Read All Appointments
@app.get("/appointments", response_model=List[AppointmentOut])
def get_appointments():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Read Single Appointment
@app.get("/appointments/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id=?", (appointment_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return dict(row)

# Update Appointment
@app.put("/appointments/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, appointment: AppointmentCreate):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id=?", (appointment_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")
    cursor.execute("""
        UPDATE appointments SET patient_name=?, age=?, condition=?, doctor_name=?
        WHERE id=?
    """, (
        appointment.patient_name,
        appointment.age,
        appointment.condition,
        appointment.doctor_name,
        appointment_id
    ))
    conn.commit()
    conn.close()
    return {**appointment.dict(), "id": appointment_id}

# Delete Appointment
@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
    conn.commit()
    conn.close()
    return {"message": f"Appointment with ID {appointment_id} deleted"}

# Get ALL Medicine
@app.get("/medicines", response_model=List[MedicineOut])
def get_medicines():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicine")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Get Medicine from ID
@app.get("/medicines/{medicine_id}", response_model=MedicineOut)
def get_medicine(medicine_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicine WHERE id = ?", (medicine_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return dict(row)

# Add Medicine
@app.post("/medicines", response_model=Medicine)
def add_medicine(med: Medicine):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medicine (name, batch_number, quantity, price_per_unit, expiry_date, stock_status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        med.name,
        med.batch_number,
        med.quantity,
        med.price_per_unit,
        med.expiry_date,
        med.stock_status
    ))
    conn.commit()
    med_id = cursor.lastrowid
    conn.close()

    return {
        **med.dict(),
        "id": med_id  
    }
    
# Update Medicine
@app.put("/medicines/{medicine_id}", response_model=MedicineOut)
def update_medicine(medicine_id: int, med: Medicine):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicine WHERE id = ?", (medicine_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Medicine not found")

    cursor.execute("""
        UPDATE medicine
        SET name=?, batch_number=?, quantity=?, price_per_unit=?, expiry_date=?, stock_status=?
        WHERE id=?
    """, (
        med.name,
        med.batch_number,
        med.quantity,
        med.price_per_unit,
        med.expiry_date,
        med.stock_status,
        medicine_id
    ))
    conn.commit()
    conn.close()

    return {
        **med.dict(),
        "id": medicine_id
    }

# Delete Medicine
@app.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicine WHERE id = ?", (medicine_id,))
    conn.commit()
    conn.close()
    return {"message": f"Medicine with ID {medicine_id} deleted"}

@app.post("/prescriptions", response_model=PrescriptionOut)
def create_prescription(prescription: PrescriptionCreate):
    conn = db.get_db()
    cursor = conn.cursor()

    # Check if the patient exists
    cursor.execute("SELECT * FROM customers WHERE id=?", (prescription.patient_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = dict(row)

    # Check if the staff member exists
    staff_id = patient["staff_id"]
    cursor.execute("SELECT * FROM staff WHERE id=?", (staff_id,))
    row1 = cursor.fetchone()
    if not row1:
        conn.close()
        raise HTTPException(status_code=404, detail="Staff not found")
    staff = dict(row1)
    # cursor.execute("""
    #     INSERT INTO prescription (patient_name, doctor_name)
    #     VALUES (?, ?)
    # """, (patient["name"], staff["name"]))
    # prescription_id = cursor.lastrowid

    # for item in prescription.items:
    #     cursor.execute("""
    #         INSERT INTO prescription_items (prescription_id, medicine_name, dosage, frequency)
    #         VALUES (?, ?, ?, ?)
    #     """, (prescription_id, item.medicine_name, item.dosage, item.frequency))

    # # Update appointment status to 'Done'
    # cursor.execute("""
    #     UPDATE customers SET status='Done' WHERE id=?
    # """, (prescription.patient_id,))

    conn.commit()
    conn.close()
    prescription_id = 0
    return {**prescription.dict(), "id": prescription_id}


@app.get("/prescriptions", response_model=List[PrescriptionOut])
def get_prescriptions():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prescription")
    prescriptions = cursor.fetchall()

    result = []
    for pres in prescriptions:
        cursor.execute("SELECT medicine_name, dosage, frequency FROM prescription_items WHERE prescription_id=?", (pres["id"],))
        items = cursor.fetchall()
        result.append({
            "id": pres["id"],
            "patient_name": pres["patient_name"],
            "doctor_name": pres["doctor_name"],
            "items": list(items)
        })

    conn.close()
    return result


@app.put("/prescriptions/{prescription_id}", response_model=PrescriptionOut)
def update_prescription(prescription_id: int, updated_prescription: PrescriptionCreate):
    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE prescription SET patient_name=?, doctor_name=? WHERE id=?", 
                   (updated_prescription.patient_name, updated_prescription.doctor_name, prescription_id))

    cursor.execute("DELETE FROM prescription_items WHERE prescription_id=?", (prescription_id,))
    for item in updated_prescription.items:
        cursor.execute("""
            INSERT INTO prescription_items (prescription_id, medicine_name, dosage, frequency)
            VALUES (?, ?, ?, ?)
        """, (prescription_id, item.medicine_name, item.dosage, item.frequency))

    conn.commit()
    conn.close()
    return {**updated_prescription.dict(), "id": prescription_id}


@app.delete("/prescriptions/{prescription_id}")
def delete_prescription(prescription_id: int):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prescription_items WHERE prescription_id=?", (prescription_id,))
    cursor.execute("DELETE FROM prescription WHERE id=?", (prescription_id,))
    conn.commit()
    conn.close()
    return {"message": f"Prescription with ID {prescription_id} deleted"}
