from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.problem import DifficultyLevel

class TestCaseBase(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool = False
    is_example: bool = False

class TestCase(TestCaseBase):
    id: int
    problem_id: int

    class Config:
        orm_mode = True

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: DifficultyLevel
    time_limit: int = 30
    memory_limit: int = 128
    starter_code: Optional[str] = None
    tags: Optional[str] = None

class ProblemCreate(ProblemBase):
    test_cases: List[TestCaseBase] = []

class Problem(ProblemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProblemWithTestCases(Problem):
    test_cases: List[TestCase] = []