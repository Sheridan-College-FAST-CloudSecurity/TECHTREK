import sqlite3

# Connect to database (or create it)
connection = sqlite3.connect("hospital.db", check_same_thread=False)

# Create a cursor to execute SQL commands
cursor = connection.cursor()

class DatabaseManagement:

    def create_table(self):
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                contact_number INTEGER,
                email TEXT,
                DOB DATE,
                gender TEXT,
                address TEXT,
                prescription_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS prescription (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                staff_id INTEGER,
                medicine_id INTEGER,
                medicine_name TEXT,
                quantity INTEGER,
                frequency TEXT,
                dosage TEXT,
                consulation_fee INTEGER
            );

            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY,
                name TEXT,
                contact_number INTEGER,
                role TEXT,
                dept TEXT,
                email TEXT
            );

            CREATE TABLE IF NOT EXISTS pharmacist (
                id INTEGER PRIMARY KEY,
                name TEXT
            );

            CREATE TABLE IF NOT EXISTS billing (
                id INTEGER PRIMARY KEY,
                name TEXT,
                customer_id INTEGER,
                pharmacist_id INTEGER,
                prescription_id INTEGER,
                total_amount INTEGER,
                payment_mode TEXT,
                transaction_id INTEGER,
                payment_status TEXT,
                payment_date DATE
            );

            CREATE TABLE IF NOT EXISTS medicine (
                id INTEGER PRIMARY KEY,
                name TEXT,
                batch_number TEXT,
                quantity TEXT,
                price_per_unit INTEGER,
                expiry_date DATE,
                stock_status TEXT
            );

            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)

        connection.commit()
        cursor.close()