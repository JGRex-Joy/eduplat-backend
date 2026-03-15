import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.sql import func
from app.database import Base


class OpportunityType(str, enum.Enum):
    internship = "internship"
    volunteering = "volunteering"
    hackathon = "hackathon"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(OpportunityType), nullable=False, index=True)
    title = Column(String, nullable=False)
    short_description = Column(String, nullable=False)
    full_description = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    event_date = Column(String, nullable=True)      # "30 Сентября"
    deadline = Column(String, nullable=True)        # "23 Марта"
    created_at = Column(DateTime(timezone=True), server_default=func.now())