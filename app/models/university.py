from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    
    min_gpa = Column(Float, nullable=True)
    avg_gpa = Column(Float, nullable=True)
    min_sat = Column(Integer, nullable=True)
    avg_sat = Column(Integer, nullable=True)
    min_ielts = Column(Float, nullable=True)
    avg_ielts = Column(Float, nullable=True)
    
    acceptance_rate = Column(Float, nullable=True)
    
    ranking = Column(Integer, nullable=True)