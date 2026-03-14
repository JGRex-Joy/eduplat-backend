from pydantic import BaseModel
from typing import Optional


class UniversityWithChanceResponse(BaseModel):
    id: int
    name: str
    country: Optional[str]
    city: Optional[str]
    min_gpa: Optional[float]
    min_sat: Optional[int]
    probability: float
    label: str
    color: str

    class Config:
        from_attributes = True