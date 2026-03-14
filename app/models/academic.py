from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AcademicInfo(Base):
    __tablename__ = "academic_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    gpa = Column(Float, nullable=False)
    sat = Column(Integer, nullable=True)
    ielts = Column(Float, nullable=True)
    toefl = Column(Float, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="academic_info")