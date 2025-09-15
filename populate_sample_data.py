import sys
sys.path.append('/home/runner/work/interview_live_coding_test/interview_live_coding_test')

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.base import Base
from app.models.problem import Problem, DifficultyLevel
from app.models.test_case import TestCase
from app.models.user import User
from app.api.auth import get_password_hash

def create_tables():
    Base.metadata.create_all(bind=engine)

def populate_sample_data():
    db = SessionLocal()
    
    try:
        # Create sample admin user
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrator",
                is_interviewer=True,
                is_active=True
            )
            db.add(admin_user)
        
        # Create sample candidate user
        candidate_user = db.query(User).filter(User.username == "candidate").first()
        if not candidate_user:
            candidate_user = User(
                username="candidate",
                email="candidate@example.com",
                hashed_password=get_password_hash("candidate123"),
                full_name="Sample Candidate",
                is_interviewer=False,
                is_active=True
            )
            db.add(candidate_user)
        
        db.commit()
        
        # Sample Problem 1: Two Sum
        problem1 = db.query(Problem).filter(Problem.title == "Two Sum").first()
        if not problem1:
            problem1 = Problem(
                title="Two Sum",
                description="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Constraints:
- 2 <= nums.length <= 104
- -109 <= nums[i] <= 109
- -109 <= target <= 109
- Only one valid answer exists.""",
                difficulty=DifficultyLevel.EASY,
                time_limit=30,
                memory_limit=128,
                starter_code="""def two_sum(nums, target):
    \"\"\"
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    \"\"\"
    # Your solution here
    pass

# Test your function
if __name__ == "__main__":
    import sys
    
    # Read input
    nums_line = input().strip()
    nums = list(map(int, nums_line.split()))
    target = int(input().strip())
    
    # Call function and print result
    result = two_sum(nums, target)
    print(result[0], result[1])""",
                tags="array,hash-table"
            )
            db.add(problem1)
            db.commit()
            db.refresh(problem1)
            
            # Test cases for Two Sum
            test_cases_1 = [
                TestCase(
                    problem_id=problem1.id,
                    input_data="2 7 11 15\n9",
                    expected_output="0 1",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem1.id,
                    input_data="3 2 4\n6",
                    expected_output="1 2",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem1.id,
                    input_data="3 3\n6",
                    expected_output="0 1",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem1.id,
                    input_data="1 2 3 4 5\n8",
                    expected_output="2 4",
                    is_example=False,
                    is_hidden=True
                )
            ]
            
            for tc in test_cases_1:
                db.add(tc)
        
        # Sample Problem 2: Palindrome Check
        problem2 = db.query(Problem).filter(Problem.title == "Valid Palindrome").first()
        if not problem2:
            problem2 = Problem(
                title="Valid Palindrome",
                description="""A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Constraints:
- 1 <= s.length <= 2 * 105
- s consists only of printable ASCII characters.""",
                difficulty=DifficultyLevel.EASY,
                time_limit=30,
                memory_limit=128,
                starter_code="""def is_palindrome(s):
    \"\"\"
    :type s: str
    :rtype: bool
    \"\"\"
    # Your solution here
    pass

# Test your function
if __name__ == "__main__":
    s = input().strip()
    result = is_palindrome(s)
    print(str(result).lower())""",
                tags="string,two-pointers"
            )
            db.add(problem2)
            db.commit()
            db.refresh(problem2)
            
            # Test cases for Palindrome
            test_cases_2 = [
                TestCase(
                    problem_id=problem2.id,
                    input_data="A man, a plan, a canal: Panama",
                    expected_output="true",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem2.id,
                    input_data="race a car",
                    expected_output="false",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem2.id,
                    input_data=" ",
                    expected_output="true",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem2.id,
                    input_data="Madam",
                    expected_output="true",
                    is_example=False,
                    is_hidden=True
                )
            ]
            
            for tc in test_cases_2:
                db.add(tc)
        
        # Sample Problem 3: FizzBuzz
        problem3 = db.query(Problem).filter(Problem.title == "FizzBuzz").first()
        if not problem3:
            problem3 = Problem(
                title="FizzBuzz",
                description="""Given an integer n, return a string array answer (1-indexed) where:

- answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
- answer[i] == "Fizz" if i is divisible by 3.
- answer[i] == "Buzz" if i is divisible by 5.
- answer[i] == i (as a string) if none of the above conditions are true.

Constraints:
- 1 <= n <= 104""",
                difficulty=DifficultyLevel.EASY,
                time_limit=30,
                memory_limit=128,
                starter_code="""def fizz_buzz(n):
    \"\"\"
    :type n: int
    :rtype: List[str]
    \"\"\"
    # Your solution here
    pass

# Test your function
if __name__ == "__main__":
    n = int(input().strip())
    result = fizz_buzz(n)
    for item in result:
        print(item)""",
                tags="math,string,simulation"
            )
            db.add(problem3)
            db.commit()
            db.refresh(problem3)
            
            # Test cases for FizzBuzz
            test_cases_3 = [
                TestCase(
                    problem_id=problem3.id,
                    input_data="3",
                    expected_output="1\n2\nFizz",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem3.id,
                    input_data="5",
                    expected_output="1\n2\nFizz\n4\nBuzz",
                    is_example=True,
                    is_hidden=False
                ),
                TestCase(
                    problem_id=problem3.id,
                    input_data="15",
                    expected_output="1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
                    is_example=True,
                    is_hidden=False
                )
            ]
            
            for tc in test_cases_3:
                db.add(tc)
        
        db.commit()
        print("Sample data populated successfully!")
        
    except Exception as e:
        print(f"Error populating data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    populate_sample_data()