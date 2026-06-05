from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from ai_services import generate_feedback

router = APIRouter()

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(
        name=student.name,
        email=student.email,
        course=student.course,
        marks=student.marks
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router.put("/students/{id}", response_model=schemas.StudentResponse)
def update_student(id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_student.name = student.name
    db_student.email = student.email
    db_student.course = student.course
    db_student.marks = student.marks
    
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

@router.get("/students/{id}/feedback")
def get_student_feedback(id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    feedback = generate_feedback(db_student)
    return {"feedback": feedback}