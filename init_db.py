import json
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.schemas import MathProblemDB

# Create tables
MathProblemDB.metadata.create_all(bind=engine)

def load_problems_from_json():
    """Load problems from ProblemSet.json into database"""
    
    db = SessionLocal()
    
    try:
        # Load JSON
        with open('ProblemSet.json', 'r') as f:
            problems = json.load(f)
        
        # Clear existing data (optional)
        db.query(MathProblemDB).delete()
        
        # Insert problems
        for problem_data in problems:
            db_problem = MathProblemDB(**problem_data)
            db.add(db_problem)
        
        db.commit()
        print(f"✅ Successfully loaded {len(problems)} problems into database!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    load_problems_from_json()