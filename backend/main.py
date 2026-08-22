from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from fastapi import Depends

import os


# ============================================================
# DATABASE CONFIGURATION
# ============================================================


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./edutech.db"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ============================================================
# DATABASE MODELS
# ============================================================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    skills = Column(String, default="")

    group_members = relationship(
        "GroupMember",
        back_populates="student"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    required_skills = Column(String, default="")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    status = Column(String, default="FORMING")

    members = relationship(
        "GroupMember",
        back_populates="group"
    )


class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    student_id = Column(Integer, ForeignKey("students.id"))

    group = relationship(
        "Group",
        back_populates="members"
    )

    student = relationship(
        "Student",
        back_populates="group_members"
    )


class GroupRequest(Base):
    __tablename__ = "group_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String, default="PENDING")


# Create database tables
Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EduConnect Peer-Group Formation API",
    description="Backend API for the scalable peer-group formation system.",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE SESSION
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class StudentCreate(BaseModel):
    name: str
    email: str
    skills: str = ""


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    skills: str

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    title: str
    description: str
    required_skills: str = ""


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    required_skills: str

    class Config:
        from_attributes = True


class GroupRequestCreate(BaseModel):
    student_id: int
    project_id: int


class GroupRequestResponse(BaseModel):
    id: int
    student_id: int
    project_id: int
    status: str

    class Config:
        from_attributes = True


class GroupResponse(BaseModel):
    id: int
    project_id: Optional[int]
    name: str
    status: str

    class Config:
        from_attributes = True


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "EduConnect Peer-Group Formation API",
        "status": "running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "peer-group-formation-api"
    }


# ============================================================
# STUDENT APIs
# ============================================================

@app.get(
    "/api/students",
    response_model=List[StudentResponse]
)
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@app.get(
    "/api/students/{student_id}",
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


@app.post(
    "/api/students",
    response_model=StudentResponse
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(Student).filter(
        Student.email == student_data.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    student = Student(
        name=student_data.name,
        email=student_data.email,
        skills=student_data.skills
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


# ============================================================
# PROJECT APIs
# ============================================================

@app.get(
    "/api/projects",
    response_model=List[ProjectResponse]
)
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@app.get(
    "/api/projects/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@app.post(
    "/api/projects",
    response_model=ProjectResponse
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    project = Project(
        title=project_data.title,
        description=project_data.description,
        required_skills=project_data.required_skills
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# ============================================================
# GROUP APIs
# ============================================================

@app.get(
    "/api/groups",
    response_model=List[GroupResponse]
)
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()


@app.get(
    "/api/groups/{group_id}",
    response_model=GroupResponse
)
def get_group(
    group_id: int,
    db: Session = Depends(get_db)
):
    group = db.query(Group).filter(
        Group.id == group_id
    ).first()

    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    return group


# ============================================================
# GROUP FORMATION REQUEST APIs
# ============================================================

@app.post(
    "/api/group-requests",
    response_model=GroupRequestResponse
)
def create_group_request(
    request_data: GroupRequestCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == request_data.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    project = db.query(Project).filter(
        Project.id == request_data.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    group_request = GroupRequest(
        student_id=request_data.student_id,
        project_id=request_data.project_id,
        status="PENDING"
    )

    db.add(group_request)
    db.commit()
    db.refresh(group_request)

    return group_request


@app.get(
    "/api/group-requests/{request_id}",
    response_model=GroupRequestResponse
)
def get_group_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    group_request = db.query(GroupRequest).filter(
        GroupRequest.id == request_id
    ).first()

    if not group_request:
        raise HTTPException(
            status_code=404,
            detail="Group request not found"
        )

    return group_request


# ============================================================
# APPLICATION STARTUP
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
