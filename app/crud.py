from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import MathProblemDB
from app.models import MathProblem

class ProblemCRUD:
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 1000) -> List[MathProblemDB]:
        return db.query(MathProblemDB).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, problem_id: str) -> Optional[MathProblemDB]:
        return db.query(MathProblemDB).filter(MathProblemDB.id == problem_id).first()
    
    @staticmethod
    def create(db: Session, problem: MathProblem) -> MathProblemDB:
        db_problem = MathProblemDB(**problem.dict())
        db.add(db_problem)
        db.commit()
        db.refresh(db_problem)
        return db_problem
    
    @staticmethod
    def update(db: Session, problem_id: str, problem: MathProblem) -> Optional[MathProblemDB]:
        db_problem = ProblemCRUD.get_by_id(db, problem_id)
        if db_problem:
            for key, value in problem.dict().items():
                setattr(db_problem, key, value)
            db.commit()
            db.refresh(db_problem)
        return db_problem
    
    @staticmethod
    def delete(db: Session, problem_id: str) -> bool:
        db_problem = ProblemCRUD.get_by_id(db, problem_id)
        if db_problem:
            db.delete(db_problem)
            db.commit()
            return True
        return False
    
    @staticmethod
    def search(
        db: Session,
        topic: Optional[str] = None,
        min_difficulty: Optional[int] = None,
        max_difficulty: Optional[int] = None,
        max_time: Optional[int] = None
    ) -> List[MathProblemDB]:
        
        query = db.query(MathProblemDB)
        
        if topic:
            # Case-insensitive search
            query = query.filter(MathProblemDB.topic.ilike(f"%{topic}%"))
        
        if min_difficulty is not None:
            query = query.filter(MathProblemDB.difficulty >= min_difficulty)
        
        if max_difficulty is not None:
            query = query.filter(MathProblemDB.difficulty <= max_difficulty)
        
        if max_time is not None:
            query = query.filter(MathProblemDB.estimated_time_to_solve_minutes <= max_time)
        
        return query.all()

crud = ProblemCRUD()