from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    code: str
    language: str = "python"

class SubmissionCreate(SubmissionBase):
    problem_id: int

class Submission(SubmissionBase):
    id: int
    user_id: int
    problem_id: int
    status: str
    execution_time: Optional[float] = None
    memory_used: Optional[int] = None
    test_cases_passed: int = 0
    total_test_cases: int = 0
    error_message: Optional[str] = None
    submitted_at: datetime

    class Config:
        orm_mode = True

class SubmissionResult(BaseModel):
    status: str
    execution_time: Optional[float] = None
    memory_used: Optional[int] = None
    test_cases_passed: int = 0
    total_test_cases: int = 0
    error_message: Optional[str] = None
    output: Optional[str] = None