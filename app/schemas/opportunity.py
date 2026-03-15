from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.opportunity import OpportunityType


class OpportunityResponse(BaseModel):
    id: int
    type: OpportunityType
    title: str
    short_description: str
    full_description: str
    image_url: Optional[str]
    event_date: Optional[str]
    deadline: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True