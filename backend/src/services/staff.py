from fastapi import FastAPI
from src.common.models import Staff
import sqlite3

app = FastAPI()

# Connect to database (or create it)
connection = sqlite3.connect("library.db", check_same_thread=False)

# Create a cursor to execute SQL commands
cursor = connection.cursor()

class StaffManagement:

    # def __init__(self, file_name="DataFiles/staff.txt"):
    #     self.file_name = file_name
    #     with open(self.file_name, "r") as f:
    #         self.staff = f

    # Retrieve All Staff from Staff.txt file using GET Method.
    def get_staff(self):
        query = "select * from staff"
        try:
            cursor.execute(query)
            staff = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in staff]
        finally:
            connection.commit()
            cursor.close()
            connection.close()

    # Add Staff details to Staff.txt file using POST Method.
    def add_staff(self, staff: Staff):
        cursor.execute("""
            INSERT INTO staff (id, name, contact_number, role, dept, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (staff.id, staff.name, staff.contact_number, staff.role, staff.dept, staff.email
        ))
        connection.commit()
        cursor.close()
        connection.close()

    # Update Staff details to Staff.txt file using PUT Method based on Staff ID
    def update_staff(self, staff_id: int, updated_staff_data: Staff):
        updated = False
        query = """update staff
                   set  name = ?, contact_number = ?, role = ?, dept = ?, email = ?
                   where id = ? """
        cursor.execute(query, (updated_staff_data.name, updated_staff_data.contact_number, updated_staff_data.role, updated_staff_data.dept, updated_staff_data.email, staff_id))
        updated = True
        connection.commit()
        cursor.close()
        connection.close()
        if not updated:
            return {"error": f"Staff '{updated_staff_data.name}' not found."}
        return {
            "msg": f"Staff '{updated_staff_data.name}' updated successfully."
        }
        if not updated:
            return {"error": f"Staff '{updated_staff_data.name}' not found."}
        return {
            "msg": f"Staff '{updated_staff_data.name}' updated successfully."
        }

    # Delete Staff details to Staff.txt file using
    # delete Method based on Staff ID
    def delete_staff(self, staff_id):
        deleted = False
        query = "delete from staff where id = ?"
        cursor.execute(query, (staff_id))
        connection.commit()
        cursor.close()
        connection.close()
        deleted = True
        if not deleted:
            return {"error": f"Staff {name} not found."}
        return {"message": f"Staff '{name}' deleted successfully."}
