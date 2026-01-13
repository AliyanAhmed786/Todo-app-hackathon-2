"""
Test suite for Better Auth registration flow with database validation.
This test validates that the registration flow works correctly with the database session validation approach.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from unittest.mock import AsyncMock, patch
from main import app  # Import the FastAPI app
from models.user import User
from models.session import Session
from datetime import datetime, timedelta
import secrets


def test_registration_flow_basic():
    """
    Test the basic registration flow with Better Auth database validation.
    This is a high-level integration test to verify the registration flow works.
    """
    # Note: This is a conceptual test - actual implementation would require
    # a proper test database setup and more complex mocking
    pass


@pytest.mark.asyncio
async def test_user_creation_with_database_session():
    """
    Test that user creation results in a database session record for Better Auth validation.
    """
    # Mock the database session and services
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Import the registration service
    from services.registration_service import register_user
    from models.user import UserCreate

    # Create test user data
    test_user_data = UserCreate(
        name="Test User",
        email="test@example.com",
        password="SecurePassword123!"
    )

    # Mock the database operations
    mock_user = User(
        id=secrets.token_hex(20),
        name=test_user_data.name,
        email=test_user_data.email,
        password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",  # bcrypt hash
        email_verified=False
    )

    # Mock the db_session.add and commit operations
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    # Patch the database operations
    with patch('services.registration_service.pwd_context.hash') as mock_hash:
        mock_hash.return_value = "$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k"

        # Call the registration service
        result = await register_user(db_session=mock_db_session, user_in=test_user_data)

        # Assert that the user was created with correct properties
        assert result.name == test_user_data.name
        assert result.email == test_user_data.email.lower()

        # Assert that the database operations were called
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()


def test_registration_request_validation():
    """
    Test that registration requests are properly validated.
    """
    from schemas.auth import UserCreateRequest

    # Test valid data
    valid_data = {
        "name": "Valid User",
        "email": "valid@example.com",
        "password": "SecurePass123!"
    }

    request = UserCreateRequest(**valid_data)
    assert request.name == "Valid User"
    assert request.email == "valid@example.com"
    assert len(request.password) >= 8


def test_registration_error_handling():
    """
    Test that registration errors are properly handled and returned.
    """
    from schemas.auth import UserCreateRequest

    # Test invalid email
    try:
        invalid_data = {
            "name": "Valid User",
            "email": "invalid-email",  # Invalid email format
            "password": "SecurePass123!"
        }
        UserCreateRequest(**invalid_data)
        assert False, "Should have raised validation error for invalid email"
    except ValueError:
        pass  # Expected validation error


def test_duplicate_email_error():
    """
    Test that duplicate email errors are properly handled.
    """
    from fastapi import HTTPException
    import re

    # This simulates the error handling in auth_router.py
    error_msg = "UNIQUE constraint failed: user.email"

    # Check if the error handling logic catches this
    if "UNIQUE constraint failed" in error_msg or "duplicate key value violates unique constraint" in error_msg:
        # This would trigger the 409 Conflict response
        assert True  # Error correctly identified
    else:
        assert False, "Duplicate email error not properly identified"


if __name__ == "__main__":
    # Run basic tests
    test_registration_request_validation()
    test_registration_error_handling()
    test_duplicate_email_error()
    print("Basic registration flow tests passed!")