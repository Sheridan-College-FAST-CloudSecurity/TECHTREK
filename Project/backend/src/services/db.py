import sqlite3

# Global DB connection (allowed with `check_same_thread=False`)
connection = sqlite3.connect("hospital.db", check_same_thread=False)

class DatabaseManagement:

    def get_db(self):
        conn = sqlite3.connect("hospital.db")
        conn.row_factory = sqlite3.Row
        return conn
        
    def create_table(self):
        cursor = connection.cursor()  # ✅ create cursor inside the method
        try:
            cursor.executescript("""                
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    contact_number TEXT,
                    email TEXT,
                    DOB TEXT,
                    gender TEXT,
                    address TEXT,
                    prescription_id INTEGER,
                    condition TEXT,
                    staff_id INTEGER,
                    status TEXT
                );

                DROP TABLE IF EXISTS prescription;
                DROP TABLE IF EXISTS prescriptions;
                DROP TABLE IF EXISTS prescription_items;
                
                CREATE TABLE IF NOT EXISTS prescriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    staff_id INTEGER,
                    consultation_fee INTEGER
                );

                CREATE TABLE IF NOT EXISTS prescription_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prescription_id INTEGER,
                    medicine_name TEXT,
                    quantity INTEGER,
                    frequency TEXT,
                    dosage TEXT
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
                );

                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    condition TEXT NOT NULL,
                    doctor_name TEXT NOT NULL
                );
            """)
            connection.commit()
        finally:
            cursor.close()  # ✅ close only the cursor you created
