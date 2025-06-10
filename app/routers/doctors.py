from fastapi import APIRouter, Query

router = APIRouter()

doctors_data = [
    {"id": 1, "name": "Dr. Smith", "specialty": "Cardiology", "email": "smith@example.com", "phone": "555-1234", "years_experience": 15, "available": True},
    {"id": 2, "name": "Dr. Jones", "specialty": "Neurology", "email": "jones@example.com", "phone": "555-5678", "years_experience": 10, "available": False},
]

@router.get("/")
def get_doctors(available: bool | None = Query(None, description="Filter by availability")):
    if available is None:
        return doctors_data
    return [doc for doc in doctors_data if doc["available"] == available]
