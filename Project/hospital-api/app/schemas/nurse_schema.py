from pydantic import BaseModel

class NurseCreate(BaseModel):
    name: str
    role: str
    phone: str
    shift: str

class NurseOut(NurseCreate):
    id: int
