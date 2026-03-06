from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class ExtracurricularCategory(str, enum.Enum):
    volunteering = "volunteering"       # Волонтерство
    leadership = "leadership"           # Лидерский опыт
    club = "club"                       # Клуб
    research = "research"               # Исследование
    olympiad = "olympiad"               # Олимпиада
    sport = "sport"                     # Спорт


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    about = relationship("UserAbout", back_populates="user", uselist=False, cascade="all, delete-orphan")
    academic_info = relationship("AcademicInfo", back_populates="user", uselist=False, cascade="all, delete-orphan")
    extracurriculars = relationship("Extracurricular", back_populates="user", cascade="all, delete-orphan")


class UserAbout(Base):
    __tablename__ = "user_about"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=True)
    school = Column(String, nullable=True)   # Место обучения
    grade = Column(String, nullable=True)    # Класс
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="about")


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


class Extracurricular(Base):
    __tablename__ = "extracurriculars"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(Enum(ExtracurricularCategory), nullable=False)
    years_active = Column(String, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="extracurriculars")