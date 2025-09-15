import pytest
import asyncio
from app.services.code_execution import CodeExecutionService

@pytest.fixture
def code_service():
    return CodeExecutionService()

@pytest.mark.asyncio
async def test_simple_code_execution(code_service):
    """Test basic code execution"""
    code = 'print("Hello World")'
    test_cases = [{"input_data": "", "expected_output": "Hello World"}]
    
    result = await code_service.execute_python_code(code, test_cases)
    
    assert result["status"] == "accepted"
    assert result["test_cases_passed"] == 1
    assert result["total_test_cases"] == 1
    assert result["error_message"] is None

@pytest.mark.asyncio
async def test_code_with_input(code_service):
    """Test code execution with input"""
    code = '''
name = input()
print(f"Hello {name}")
'''
    test_cases = [{"input_data": "World", "expected_output": "Hello World"}]
    
    result = await code_service.execute_python_code(code, test_cases)
    
    assert result["status"] == "accepted"
    assert result["test_cases_passed"] == 1

@pytest.mark.asyncio
async def test_code_with_error(code_service):
    """Test code execution with runtime error"""
    code = '''
x = 1 / 0  # Division by zero
'''
    test_cases = [{"input_data": "", "expected_output": ""}]
    
    result = await code_service.execute_python_code(code, test_cases)
    
    assert result["status"] == "runtime_error"
    assert result["test_cases_passed"] == 0
    assert "division by zero" in result["error_message"].lower()

@pytest.mark.asyncio
async def test_wrong_answer(code_service):
    """Test code execution with wrong output"""
    code = 'print("Wrong Answer")'
    test_cases = [{"input_data": "", "expected_output": "Correct Answer"}]
    
    result = await code_service.execute_python_code(code, test_cases)
    
    assert result["status"] == "wrong_answer"
    assert result["test_cases_passed"] == 0
    assert result["total_test_cases"] == 1

@pytest.mark.asyncio
async def test_two_sum_solution(code_service):
    """Test a working Two Sum solution"""
    code = '''
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

if __name__ == "__main__":
    nums_line = input().strip()
    nums = list(map(int, nums_line.split()))
    target = int(input().strip())
    result = two_sum(nums, target)
    print(result[0], result[1])
'''
    
    test_cases = [
        {"input_data": "2 7 11 15\n9", "expected_output": "0 1"},
        {"input_data": "3 2 4\n6", "expected_output": "1 2"}
    ]
    
    result = await code_service.execute_python_code(code, test_cases)
    
    assert result["status"] == "accepted"
    assert result["test_cases_passed"] == 2
    assert result["total_test_cases"] == 2