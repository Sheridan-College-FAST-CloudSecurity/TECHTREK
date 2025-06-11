from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str
    description: str

class DepartmentOut(DepartmentCreate):
    id: int
