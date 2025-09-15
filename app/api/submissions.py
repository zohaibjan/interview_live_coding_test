from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.submission import Submission
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.user import User
from app.schemas.submission import SubmissionCreate, Submission as SubmissionSchema, SubmissionResult
from app.api.auth import get_current_user
from app.services.code_execution import CodeExecutionService

router = APIRouter()
code_execution_service = CodeExecutionService()

@router.post("/", response_model=SubmissionResult)
async def submit_code(
    submission: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Get test cases for this problem
    test_cases = db.query(TestCase).filter(TestCase.problem_id == submission.problem_id).all()
    
    if not test_cases:
        raise HTTPException(status_code=400, detail="No test cases found for this problem")
    
    # Convert test cases to the format expected by code execution service
    test_case_data = [
        {
            "input_data": tc.input_data,
            "expected_output": tc.expected_output
        }
        for tc in test_cases
    ]
    
    # Execute the code
    if submission.language == "python":
        execution_result = await code_execution_service.execute_python_code(
            submission.code, 
            test_case_data
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    # Create submission record
    db_submission = Submission(
        user_id=current_user.id,
        problem_id=submission.problem_id,
        code=submission.code,
        language=submission.language,
        status=execution_result["status"],
        execution_time=execution_result.get("execution_time"),
        memory_used=execution_result.get("memory_used"),
        test_cases_passed=execution_result.get("test_cases_passed", 0),
        total_test_cases=execution_result.get("total_test_cases", 0),
        error_message=execution_result.get("error_message")
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    # Return result
    return SubmissionResult(
        status=execution_result["status"],
        execution_time=execution_result.get("execution_time"),
        memory_used=execution_result.get("memory_used"),
        test_cases_passed=execution_result.get("test_cases_passed", 0),
        total_test_cases=execution_result.get("total_test_cases", 0),
        error_message=execution_result.get("error_message"),
        output=str(execution_result.get("outputs", ""))
    )

@router.get("/", response_model=List[SubmissionSchema])
def get_my_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return submissions

@router.get("/problem/{problem_id}", response_model=List[SubmissionSchema])
def get_submissions_for_problem(
    problem_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.problem_id == problem_id
    ).offset(skip).limit(limit).all()
    return submissions

@router.get("/{submission_id}", response_model=SubmissionSchema)
def get_submission(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    submission = db.query(Submission).filter(
        Submission.id == submission_id,
        Submission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return submission