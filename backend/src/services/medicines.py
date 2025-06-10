from fastapi import FastAPI
from src.common.models import Medicine
import sqlite3

app = FastAPI()

# Connect to database (or create it)
connection = sqlite3.connect("library.db", check_same_thread=False)

# Create a cursor to execute SQL commands
cursor = connection.cursor()

class MedicineManagement:

    # def __init__(self, file_name="DataFiles/medicine.txt"):
    #     self.file_name = file_name
    #     with open(self.file_name, "r") as f:
    #         self.medicine = f

    # Retrieve All Medicines from Medicine.txt file using GET Method.
    def get_medicines(self):
        query = "select * from medicine"
        try:
            cursor.execute(query)
            medicines = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in medicines]
        finally:
            connection.commit()

    # Add Medicine details to Medicine.txt file using POST Method.
    def add_medicine(self, medicine: Medicine):
        cursor.execute("""
            INSERT INTO medicine (id, name, batch_number, quantity, price_per_unit, expiry_date, stock_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (medicine.id, medicine.name, medicine.batch_number, medicine.quantity, medicine.price_per_unit, medicine.expiry_date, medicine.stock_status
        ))
        connection.commit()
        return {"msg": f"Medicine '{medicine.name}' added successfully."}

    # Update details to Medicine.txt file using
    # PUT Method based on Medicine ID
    def update_medicine(self, medicine_id: int, updated_med_data: Medicine):
        updated = False
        query = """update medicine
                   set  name = ?, batch_number = ?, quantity = ?, price_per_unit = ?, expiry_date = ?, stock_status = ?
                   where id = ? """
        cursor.execute(query, (updated_med_data.name, updated_med_data.batch_number, updated_med_data.quantity, updated_med_data.price_per_unit,updated_med_data.expiry_date, updated_med_data.stock_status, medicine_id))
        updated = True
        connection.commit()
        if not updated:
            return {"error": f"Medicine '{updated_med_data.name}' not found."}
        return {
            "msg": f"Medicine '{updated_med_data.name}' updated successfully."
        }

    def delete_medicine(self, medicine_id):
        deleted = False
        query = "delete from medicine where id = ?"
        cursor.execute(query, (medicine_id))
        connection.commit()
        if not deleted:
            return {"error": f"Medicine {name} not found."}
        return {"message": f"Medicine '{name}' deleted successfully."}
