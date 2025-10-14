from pydantic import BaseModel
from typing import List
from enum import Enum

class MathProblem(BaseModel):
    id: str
    text: str
    topic: str
    difficulty: int
    estimated_time_to_solve_minutes: int
    
    class Config:
        from_attributes = True

class StudentProfile(BaseModel):
    id: str
    mastered_topics: List[str]
    learning_goals: List[str]

class PedagogicalStrategy(str, Enum):
    REVIEW = "REVIEW"
    NEW_TOPIC_INTRODUCTION = "NEW_TOPIC_INTRODUCTION"
    CHALLENGE = "CHALLENGE"

class AssessmentRequest(BaseModel):
    max_total_time_minutes: int
    pedagogical_strategy: PedagogicalStrategy

class GenerateAssessmentInput(BaseModel):
    student_profile: StudentProfile
    assessment_request: AssessmentRequest

class ProblemCriteria(BaseModel):
    topic: str
    difficulty_range: List[int]
    count: int
    time_budget_minutes: int

class AssessmentPlan(BaseModel):
    strategy: str
    reasoning: List[str]
    problem_selection_criteria: List[ProblemCriteria]

class GeneratedAssessment(BaseModel):
    assessment_id: str
    planner_output: AssessmentPlan
    selected_problems: List[MathProblem]
    total_estimated_time_minutes: int
    total_problems: int