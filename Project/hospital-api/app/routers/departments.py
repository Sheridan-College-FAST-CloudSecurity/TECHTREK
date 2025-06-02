from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_departments():
    return {"message": "List of departments"}
