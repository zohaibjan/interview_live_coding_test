from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.user import User
from app.schemas.problem import Problem as ProblemSchema, ProblemCreate, ProblemWithTestCases
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProblemSchema])
def list_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    problems = db.query(Problem).offset(skip).limit(limit).all()
    return problems

@router.get("/{problem_id}", response_model=ProblemWithTestCases)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Get example test cases (not hidden ones)
    test_cases = db.query(TestCase).filter(
        TestCase.problem_id == problem_id,
        TestCase.is_hidden == False
    ).all()
    
    problem.test_cases = test_cases
    return problem

@router.post("/", response_model=ProblemSchema)
def create_problem(
    problem: ProblemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only interviewers can create problems
    if not current_user.is_interviewer:
        raise HTTPException(status_code=403, detail="Only interviewers can create problems")
    
    db_problem = Problem(
        title=problem.title,
        description=problem.description,
        difficulty=problem.difficulty,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit,
        starter_code=problem.starter_code,
        tags=problem.tags
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    # Add test cases
    for test_case_data in problem.test_cases:
        test_case = TestCase(
            problem_id=db_problem.id,
            input_data=test_case_data.input_data,
            expected_output=test_case_data.expected_output,
            is_hidden=test_case_data.is_hidden,
            is_example=test_case_data.is_example
        )
        db.add(test_case)
    
    db.commit()
    return db_problem