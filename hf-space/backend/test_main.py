import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo App Backend API"}

def test_health_check():
    """
    Test the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "Todo App Backend API is running"}

def test_auth_signup_missing_data():
    """
    Test signup endpoint with missing data.
    """
    response = client.post("/auth/signup", json={})
    # Should return 422 for validation error or 400 for bad request
    assert response.status_code in [422, 400]

def test_auth_login_missing_data():
    """
    Test login endpoint with missing data.
    """
    response = client.post("/auth/login", json={})
    # Should return 422 for validation error or 400 for bad request
    assert response.status_code in [422, 400]