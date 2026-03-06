from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AcademicInfo(Base):
    __tablename__ = "academic_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    gpa = Column(Float, nullable=True)
    sat = Column(Integer, nullable=True)
    ielts_toefl = Column(Float, nullable=True)
    act = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="academic_info")