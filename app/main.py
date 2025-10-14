from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import engine, get_db
from app.schemas import MathProblemDB
from app.models import (
    MathProblem, GenerateAssessmentInput, GeneratedAssessment
)
from app.crud import crud
from app.planner import Planner
from app.executor import Executor

# Create database tables
MathProblemDB.metadata.create_all(bind=engine)

app = FastAPI(
    title="Adaptive Learning Orchestrator",
    version="1.0.0",
    description="An intelligent assessment generation system"
)

planner = Planner()
executor = Executor()

# ============== HEALTH CHECK ==============

@app.get("/")
def root():
    return {
        "message": "Adaptive Learning Orchestrator API",
        "status": "running",
        "docs": "/docs"
    }

# ============== CRUD ENDPOINTS ==============

@app.get("/api/problems", response_model=List[MathProblem])
def get_all_problems(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get all problems with pagination"""
    problems = crud.get_all(db, skip=skip, limit=limit)
    return problems

@app.get("/api/problems/{problem_id}", response_model=MathProblem)
def get_problem(problem_id: str, db: Session = Depends(get_db)):
    """Get a single problem by ID"""
    problem = crud.get_by_id(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.post("/api/problems", response_model=MathProblem, status_code=201)
def create_problem(problem: MathProblem, db: Session = Depends(get_db)):
    """Create a new problem"""
    if crud.get_by_id(db, problem.id):
        raise HTTPException(status_code=400, detail="Problem ID already exists")
    return crud.create(db, problem)

@app.put("/api/problems/{problem_id}", response_model=MathProblem)
def update_problem(
    problem_id: str, 
    problem: MathProblem, 
    db: Session = Depends(get_db)
):
    """Update an existing problem"""
    updated = crud.update(db, problem_id, problem)
    if not updated:
        raise HTTPException(status_code=404, detail="Problem not found")
    return updated

@app.delete("/api/problems/{problem_id}")
def delete_problem(problem_id: str, db: Session = Depends(get_db)):
    """Delete a problem"""
    success = crud.delete(db, problem_id)
    if not success:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {"message": "Problem deleted successfully", "id": problem_id}

# ============== SEARCH ENDPOINT ==============

@app.get("/api/problems/search", response_model=List[MathProblem])
def search_problems(
    topic: str = None,
    min_difficulty: int = None,
    max_difficulty: int = None,
    max_time: int = None,
    db: Session = Depends(get_db)
):
    """Search problems with filters"""
    results = crud.search(db, topic, min_difficulty, max_difficulty, max_time)
    return [MathProblem.from_orm(p) for p in results]

# ============== MAIN ASSESSMENT GENERATION ENDPOINT ==============

@app.post("/api/assessments/generate", response_model=GeneratedAssessment)
def generate_assessment(
    input_data: GenerateAssessmentInput,
    db: Session = Depends(get_db)
):
    """
    Generate a personalized assessment
    
    Flow:
    1. Planner analyzes student profile and creates a plan
    2. Executor executes the plan by selecting problems
    3. Return complete assessment with reasoning
    """
    
    # Step 1: Planner creates the strategic plan
    plan = planner.create_plan(
        input_data.student_profile,
        input_data.assessment_request
    )
    
    # Step 2: Executor executes the plan
    selected_problems = executor.execute_plan(db, plan)
    
    # Step 3: Calculate metadata
    total_time = sum(p.estimated_time_to_solve_minutes for p in selected_problems)
    
    # Step 4: Return complete assessment
    return GeneratedAssessment(
        assessment_id=str(uuid.uuid4()),
        planner_output=plan,
        selected_problems=selected_problems,
        total_estimated_time_minutes=total_time,
        total_problems=len(selected_problems)
    )