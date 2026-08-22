from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentBase(BaseModel):
    student_id: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    interests: Optional[str] = ""

    skills: Optional[str] = ""

    skill_level: str = "BEGINNER"


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )

    email: Optional[EmailStr] = None

    interests: Optional[str] = None

    skills: Optional[str] = None

    skill_level: Optional[str] = None


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
