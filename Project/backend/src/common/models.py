from datetime import date
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from typing import List

class Customer(BaseModel):
    name: str
    contact_number: str
    email: str
    DOB: date
    gender: str
    address: str
    prescription_id: Optional[int] = None
    condition: str
    staff_id: int
    status: str

class Billing(BaseModel):
    id: int
    name: str
    customer_id: int
    pharmacist_id: int
    prescription_id: int
    total_amount: int
    payment_mode: str
    transaction_id: int
    payment_status: str
    payment_date: date

class Medicine(BaseModel):

    name: str
    batch_number: str
    quantity: int
    price_per_unit: int
    expiry_date: date
    stock_status: str

class Pharmacist(BaseModel):
    id: int
    name: str
    
class Prescription(BaseModel):
    id: int
    customer_id: int
    staff_id: int
    medicine_id: int
    medicine_name: str
    quantity: int
    frequency: str
    dosage: str
    consulation_fee: int

class Staff(BaseModel):
    name: str
    contact_number: constr(min_length=10, max_length=15)  # validates length
    role: str
    dept: str
    email: EmailStr

class StaffOut(Staff):
    id: int

class MedicineOut(Medicine):
    id: int
    
class PatientOut(Customer):
    id: int

class AppointmentBase(BaseModel):
    patient_name: str
    age: int
    condition: str
    doctor_name: str

class AppointmentCreate(AppointmentBase):
    pass  # For now, same fields as base

class AppointmentOut(AppointmentBase):
    id: int

class PrescriptionItem(BaseModel):
    medicine_name: str
    dosage: str
    frequency: str

class PrescriptionCreate(BaseModel):
    patient_name: str
    doctor_name: str
    items: List[PrescriptionItem] 

class PrescriptionOut(PrescriptionCreate):
    id: int