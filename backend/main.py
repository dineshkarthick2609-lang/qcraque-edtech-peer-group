from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import engine, get_db
from models import Base, Student
from schemas import StudentCreate, StudentUpdate, StudentResponse


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EduConnect Peer-Group Formation API",
    description="Backend API for the EduConnect Peer-Group Formation System",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "EduConnect API is running",
        "version": "1.0.0"
    }


# ============================================================
# CREATE STUDENT
# POST /students
# ============================================================

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=201
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(Student).filter(
        (Student.student_id == student.student_id) |
        (Student.email == student.email)
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="Student ID or email already exists"
        )

    new_student = Student(
        student_id=student.student_id,
        name=student.name,
        email=student.email,
        interests=student.interests,
        skills=student.skills,
        skill_level=student.skill_level
    )

    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Student could not be created because the data already exists"
        )


# ============================================================
# GET ALL STUDENTS
# GET /students
# ============================================================

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):
    students = db.query(Student).order_by(
        Student.id
    ).all()

    return students


# ============================================================
# GET STUDENT BY ID
# GET /students/{student_id}
# ============================================================

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ============================================================
# UPDATE STUDENT
# PUT /students/{student_id}
# ============================================================

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)

        return student

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )


# ============================================================
# DELETE STUDENT
# DELETE /students/{student_id}
# ============================================================

@app.delete(
    "/students/{student_id}"
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }
