import random
from typing import List
from sqlalchemy.orm import Session
from app.models import AssessmentPlan, MathProblem
from app.crud import crud

class Executor:
    """
    The Executor: Executes the plan without making decisions
    """
    
    def execute_plan(self, db: Session, plan: AssessmentPlan) -> List[MathProblem]:
        selected_problems = []
        
        for criteria in plan.problem_selection_criteria:
            # Search database for matching problems
            matching_problems = crud.search(
                db=db,
                topic=criteria.topic,
                min_difficulty=criteria.difficulty_range[0],
                max_difficulty=criteria.difficulty_range[1],
                max_time=criteria.time_budget_minutes
            )
            
            # Convert SQLAlchemy models to Pydantic models
            matching_pydantic = [MathProblem.from_orm(p) for p in matching_problems]
            
            # Randomly select specified count
            num_to_select = min(criteria.count, len(matching_pydantic))
            if num_to_select > 0:
                selected = random.sample(matching_pydantic, num_to_select)
                selected_problems.extend(selected)
        
        return selected_problems