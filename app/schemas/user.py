from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.schemas.academic import AcademicInfoResponse
from app.schemas.extracurricular import ExtracurricularResponse


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