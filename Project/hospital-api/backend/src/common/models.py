from datetime import date
from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    name: str
    contact_number: str
    email: str
    DOB: date
    gender: str
    address: str
    prescription_id: int

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
    id: int
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
    id: int
    name: str
    contact_number: int
    role: str
    dept: str
    email: str
