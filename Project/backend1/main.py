import logging
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
from src.services.db import DatabaseManagement

app = FastAPI()

origins = [
    "https://glorious-space-fishstick-pjpgxxpr9qgxc79qp-8080.app.github.dev"
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
    logger.info("Testing123")
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