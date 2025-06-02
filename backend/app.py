import logging
from fastapi import FastAPI
from src.services.medicines import MedicineManagement
from src.services.customer import CustomerManagement
from src.services.staff import StaffManagement
from src.services.db import DatabaseManagement
from src.common.models import Medicine, Customer, Staff
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (React) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React runs on port 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_management = DatabaseManagement()
medicine_management = MedicineManagement()
customer_management = CustomerManagement()
staff_management = StaffManagement()

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

@app.get("/create_table")
def create_table():
    logger.info("All table created")
    return database_management.create_table()


# GET endpoint to retrieve medicines
@app.get("/medicines")
def get_medicines():
    logger.info("GET Request: /medicines - Fetch all data of medicine.")
    return medicine_management.get_medicines()


# POST endpoint to add medicine
@app.post("/medicines")
def add_medicine(medicine: Medicine):
    logger.info("POST Request: Medicine information will be added.")
    return medicine_management.add_medicine(medicine)


# PUT endpoint to update the medicine details
@app.put("/medicines/{medicine_id}")
def update_medicine(medicine_id: int, medicine: Medicine):
    updated = medicine_management.update_medicine(medicine_id, medicine)
    logger.info("PUT Request: Medicine information will be Updated.")
    if not updated:
        logging.error(f"PUT /medicines/{medicine_id} - Not Found.")
    return updated


# for deleting the medicine info
@app.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int):
    deleted = medicine_management.delete_medicine(medicine_id)
    logger.info("DELETE Request: Medicine information will be deleted.")
    if not deleted:
        logging.error(f"DELETE /medicines/{medicine_id} - Not Found.")
    return deleted


# ----------------------- Customer API--------------------------------


# GET endpoint to retrieve customer
@app.get("/customers")
def get_customer():
    logger.info("GET Request: /Customer - Fetch all data of Customer.")
    return customer_management.get_customers()


# POST endpoint to add customer
@app.post("/customers")
def add_customer(customer: Customer):
    logger.info("POST Request: Customer information will be added.")
    return customer_management.add_customer(customer)


# PUT endpoint to update the customer details
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    updated = customer_management.update_customer(customer_id, customer)
    logger.info("PUT Request: Customer information will be Updated.")
    if not updated:
        logging.error(f"PUT /customers/{customer_id} - Not Found.")
    return updated


# for deleting the customer info
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    deleted = customer_management.delete_customer(customer_id)
    logger.info("DELETE Request: Customer information will be deleted.")
    if not deleted:
        logging.error(f"DELETE /customers/{customer_id} - Not Found.")
    return deleted


# ------------------------------- Staff API------------------------------------


# GET endpoint to retrieve customer
@app.get("/staff")
def get_staff():
    logger.info("GET Request: /staff - Fetch all data of staff.")
    return staff_management.get_staff()


# POST endpoint to add staff
@app.post("/staff")
def add_staff(staff: Staff):
    logger.info("POST Request: Staff information will be added.")
    return staff_management.add_staff(staff)


# PUT endpoint to update the medicine details
@app.put("/staff/{staff_id}")
def update_staff(staff_id: int, staff: Staff):
    updated = staff_management.update_staff(staff_id, staff)
    logger.info("PUT Request: Staff information will be updated.")
    if not updated:
        logging.error(f"PUT /staff/{staff_id} - Not Found.")
    return updated


# for deleting the staff info
@app.delete("/staff/{staff_id}")
def delete_staff(staff_id: int):
    deleted = staff_management.delete_staff(staff_id)
    logger.info("DELETE Request: Staff information will be deleted.")
    if not deleted:
        logging.error(f"DELETE /staff/{staff_id} - Not Found.")
    return deleted