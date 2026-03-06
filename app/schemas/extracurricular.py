import re
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.extracurricular import ExtracurricularCategory


class ExtracurricularCreate(BaseModel):
    categories: List[ExtracurricularCategory]
    years_active: Optional[str] = None

    @field_validator("years_active")
    @classmethod
    def validate_years(cls, v):
        if v is not None and not re.match(r"^\d{4}(-\d{4})?$", v):
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