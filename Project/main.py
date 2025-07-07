from fastapi import FastAPI
from app.database import engine 
from app.routers import dashboard

app = FastAPI()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to my Capstone API"}

# Example: GET /items/{item_id}
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}
