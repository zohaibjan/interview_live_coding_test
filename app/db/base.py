# Import all the models here to make sure they are registered with SQLAlchemy
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.test_case import TestCase
from app.db.database import Base