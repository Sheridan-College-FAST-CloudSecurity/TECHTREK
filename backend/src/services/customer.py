from fastapi import FastAPI
from src.common.models import Customer
import sqlite3

app = FastAPI()

# Connect to database (or create it)
connection = sqlite3.connect("library.db", check_same_thread=False)

# Create a cursor to execute SQL commands
cursor = connection.cursor()

class CustomerManagement:

    # def __init__(self, file_name="DataFiles/customer.txt"):
    #     self.file_name = file_name
    #     with open(self.file_name, "r") as f:
    #         self.customer = f

    # Add Customer details to Customer.txt file using POST Method.
    def add_customer(self, customer: Customer):
        cursor.execute("""
            INSERT INTO customers (id, name, contact_number, email, DOB, gender, address, prescription_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (customer.id, customer.name, customer.contact_number, customer.email, customer.DOB, customer.gender, customer.address, customer.prescription_id
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return {"msg": f"Customer '{customer.name}' added successfully."}

    # Retrieve All Customers from Customer.txt file using GET Method.
    def get_customers(self):
        query = "select * from customers"
        try:
            cursor.execute(query)
            customers = cursor.fetchall()
            return [dict(zip([column[0] for column in cursor.description], row)) for row in customers]
        finally:
            connection.commit()
            cursor.close()
            connection.close()

    # Update Customer details to Customer.txt file using
    # PUT Method based on Customer ID
    def update_customer(self, customer_id: int, updated_cust_data: Customer):
        updated = False
        query = """update customers
                   set  name = ?, contact_number = ?, email = ?, DOB = ?, gender = ?, address = ?, prescription_id = ?
                   where id = ? """
        cursor.execute(query, (updated_cust_data.name, updated_cust_data.contact_number, updated_cust_data.email, updated_cust_data.DOB, updated_cust_data.gender, updated_cust_data.address, updated_cust_data.prescription_id, customer_id))
        updated = True
        connection.commit()
        cursor.close()
        connection.close()
        if not updated:
            return {"error": f"Customer '{updated_cust_data.name}' not found."}
        return {
            "msg": f"Customer '{updated_cust_data.name}' updated successfully."
        }

    # Delete Customer details to Customer.txt file using
    # delete Method based on Customer ID
    def delete_customer(self, customer_id):
        deleted = False
        query = "delete from customers where id = ?"
        cursor.execute(query, (customer_id))
        connection.commit()
        cursor.close()
        connection.close()
        if not deleted:
            return {"error": f"Customer {name} not found."}
        return {"message": f"Customer '{name}' deleted successfully."}
