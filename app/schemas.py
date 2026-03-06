from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from app.models import ExtracurricularCategory


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Пароли не совпадают")
        return v


class UserAboutCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    school: Optional[str] = None
    grade: Optional[str] = None


class UserAboutUpdate(UserAboutCreate):
    pass


class UserAboutResponse(BaseModel):
    id: int
    user_id: int
    name: Optional[str]
    school: Optional[str]
    grade: Optional[str]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


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


class ExtracurricularCreate(BaseModel):
    categories: List[ExtracurricularCategory]
    years_active: Optional[str] = None

    @field_validator("years_active")
    @classmethod
    def validate_years(cls, v):
        if v is not None:
            import re
            if not re.match(r"^\d{4}(-\d{4})?$", v):
                raise ValueError("Формат лет: YYYY или YYYY-YYYY, например: 2020-2025")
        return v


class ExtracurricularResponse(BaseModel):
    id: int
    user_id: int
    category: ExtracurricularCategory
    years_active: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    about: Optional[UserAboutResponse]
    academic_info: Optional[AcademicInfoResponse]
    extracurriculars: List[ExtracurricularResponse]

    class Config:
        from_attributes = True