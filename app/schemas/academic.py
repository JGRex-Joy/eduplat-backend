from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class AcademicInfoCreate(BaseModel):
    gpa: Optional[float] = None
    sat: Optional[int] = None
    ielts_toefl: Optional[float] = None
    act: Optional[int] = None

    @field_validator("gpa")
    @classmethod
    def validate_gpa(cls, v):
        if v is not None and not (0.0 <= v <= 4.0):
            raise ValueError("GPA должен быть в диапазоне 0.00–4.00")
        return v

    @field_validator("sat")
    @classmethod
    def validate_sat(cls, v):
        if v is not None and not (400 <= v <= 1600):
            raise ValueError("SAT должен быть в диапазоне 400–1600")
        return v

    @field_validator("ielts_toefl")
    @classmethod
    def validate_ielts_toefl(cls, v):
        if v is not None and not (0 <= v <= 120):
            raise ValueError("IELTS/TOEFL должен быть в диапазоне 0–120 или 1.0–9.0")
        return v

    @field_validator("act")
    @classmethod
    def validate_act(cls, v):
        if v is not None and not (1 <= v <= 36):
            raise ValueError("ACT должен быть в диапазоне 1–36")
        return v


class AcademicInfoUpdate(AcademicInfoCreate):
    pass


class AcademicInfoResponse(BaseModel):
    id: int
    user_id: int
    gpa: Optional[float]
    sat: Optional[int]
    ielts_toefl: Optional[float]
    act: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True