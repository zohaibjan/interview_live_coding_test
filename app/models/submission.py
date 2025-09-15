from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String, default="python", nullable=False)
    status = Column(String, nullable=False)  # "pending", "accepted", "wrong_answer", "time_limit_exceeded", "runtime_error"
    execution_time = Column(Float, nullable=True)  # in seconds
    memory_used = Column(Integer, nullable=True)  # in MB
    test_cases_passed = Column(Integer, default=0)
    total_test_cases = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    problem = relationship("Problem")