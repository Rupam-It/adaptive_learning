from app.models import (
    StudentProfile, AssessmentRequest, AssessmentPlan, 
    ProblemCriteria, PedagogicalStrategy
)

class Planner:
    """
    The Planner: Decides WHAT to do based on student needs
    """
    
    def create_plan(self, student_profile: StudentProfile, 
                    assessment_request: AssessmentRequest) -> AssessmentPlan:
        
        strategy = assessment_request.pedagogical_strategy
        max_time = assessment_request.max_total_time_minutes
        
        reasoning = []
        criteria = []
        
        if strategy == PedagogicalStrategy.REVIEW:
            reasoning.append("Student requested review of mastered topics")
            reasoning.append(f"Mastered topics: {', '.join(student_profile.mastered_topics)}")
            
            time_per_topic = max_time // len(student_profile.mastered_topics) if student_profile.mastered_topics else max_time
            
            for topic in student_profile.mastered_topics:
                criteria.append(ProblemCriteria(
                    topic=topic,
                    difficulty_range=[1, 3],  # Easy to medium
                    count=3,
                    time_budget_minutes=time_per_topic
                ))
        
        elif strategy == PedagogicalStrategy.NEW_TOPIC_INTRODUCTION:
            reasoning.append("Introducing new topics to the student")
            reasoning.append(f"Learning goals: {', '.join(student_profile.learning_goals)}")
            
            time_per_topic = max_time // len(student_profile.learning_goals) if student_profile.learning_goals else max_time
            
            for topic in student_profile.learning_goals:
                criteria.append(ProblemCriteria(
                    topic=topic,
                    difficulty_range=[1, 2],  # Start easy
                    count=2,
                    time_budget_minutes=time_per_topic
                ))
        
        elif strategy == PedagogicalStrategy.CHALLENGE:
            reasoning.append("Providing challenging problems for mastered topics")
            reasoning.append(f"Challenge topics: {', '.join(student_profile.mastered_topics)}")
            
            time_per_topic = max_time // len(student_profile.mastered_topics) if student_profile.mastered_topics else max_time
            
            for topic in student_profile.mastered_topics:
                criteria.append(ProblemCriteria(
                    topic=topic,
                    difficulty_range=[3, 5],  # Hard problems
                    count=2,
                    time_budget_minutes=time_per_topic
                ))
        
        return AssessmentPlan(
            strategy=strategy.value,
            reasoning=reasoning,
            problem_selection_criteria=criteria
        )