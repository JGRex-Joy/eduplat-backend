from pydantic import BaseModel, field_validator
from typing import List


class MotivationLetterRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        v = v.strip()
        if len(v) < 100:
            raise ValueError("Мотивационное письмо должно содержать минимум 100 символов")
        if len(v) > 10_000:
            raise ValueError("Мотивационное письмо не должно превышать 10 000 символов")
        return v


class MotivationLetterResponse(BaseModel):
    score: int             
    label: str          
    color: str          
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]