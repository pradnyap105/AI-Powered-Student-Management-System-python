from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    course: str
    marks: int

class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True