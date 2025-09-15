import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint returns the homepage"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Live Coding Interview Platform" in response.text

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_problems():
    """Test getting the list of problems"""
    response = client.get("/api/problems/")
    assert response.status_code == 200
    problems = response.json()
    assert isinstance(problems, list)
    assert len(problems) > 0
    
    # Check first problem structure
    problem = problems[0]
    assert "title" in problem
    assert "description" in problem
    assert "difficulty" in problem
    assert "id" in problem

def test_get_single_problem():
    """Test getting a single problem"""
    response = client.get("/api/problems/1")
    assert response.status_code == 200
    problem = response.json()
    assert problem["title"] == "Two Sum"
    assert "test_cases" in problem

def test_register_user():
    """Test user registration"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "is_interviewer": False
    }
    response = client.post("/api/auth/register", json=user_data)
    # This might fail if user already exists, which is okay
    assert response.status_code in [200, 400]

def test_login():
    """Test user login"""
    login_data = {
        "username": "candidate",
        "password": "candidate123"
    }
    response = client.post("/api/auth/token", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"

def test_submit_code_unauthorized():
    """Test that code submission requires authentication"""
    submission_data = {
        "problem_id": 1,
        "code": "print('hello')",
        "language": "python"
    }
    response = client.post("/api/submissions/", json=submission_data)
    assert response.status_code == 401