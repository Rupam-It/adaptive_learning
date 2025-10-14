from sqlalchemy import Column, String, Integer
from app.database import Base

class MathProblemDB(Base):
    __tablename__ = "math_problems"
    
    id = Column(String, primary_key=True, index=True)
    text = Column(String, nullable=False)
    topic = Column(String, nullable=False, index=True)
    difficulty = Column(Integer, nullable=False, index=True)
    estimated_time_to_solve_minutes = Column(Integer, nullable=False)