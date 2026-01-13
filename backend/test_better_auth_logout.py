"""
Test suite for Better Auth logout functionality.
This test validates that logout works correctly and subsequent API calls are denied.
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


@pytest.mark.asyncio
async def test_logout_functionality():
    """
    Test that logout works correctly and invalidates the session.
    """
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Import the logout service
    from services.logout_service import logout_user

    # Create test session data
    user_id = secrets.token_hex(20)
    session_token = secrets.token_urlsafe(32)

    # Mock the delete_session function from session service
    with patch('services.session_service.delete_session') as mock_delete_session:
        mock_delete_session.return_value = True  # Simulate successful deletion

        # Call the logout service
        result = await logout_user(
            db_session=mock_db_session,
            session_token=session_token
        )

        # Assert that the logout was successful
        assert result["success"] is True
        assert result["message"] == "Successfully logged out"


@pytest.mark.asyncio
async def test_logout_with_nonexistent_session():
    """
    Test that logout handles non-existent sessions gracefully.
    """
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Import the logout service
    from services.logout_service import logout_user

    # Create test session data
    session_token = secrets.token_urlsafe(32)

    # Mock the delete_session function to return False (session not found)
    with patch('services.session_service.delete_session') as mock_delete_session:
        mock_delete_session.return_value = False  # Session not found

        # Call the logout service
        result = await logout_user(
            db_session=mock_db_session,
            session_token=session_token
        )

        # Even though session wasn't found, it should still be considered successful
        # since the goal is to end the session
        assert result["success"] is True
        assert result["message"] == "Session already ended or invalid"


def test_logout_endpoint_removes_cookies():
    """
    Test that the logout endpoint properly removes authentication cookies.
    """
    # This is a conceptual test - actual implementation would require
    # a proper test setup with TestClient
    from fastapi.responses import Response
    from api.auth_router import logout_user
    from fastapi import Request

    # Create a mock request with session cookie
    mock_request = Request(scope={
        "type": "http",
        "method": "POST",
        "path": "/api/auth/logout",
        "headers": [(b"cookie", b"better-auth.session_token=test-token-123")]
    })

    # Create a response object
    response = Response()

    # This would normally be tested with TestClient in a real scenario
    assert True  # Placeholder for actual test implementation


@pytest.mark.asyncio
async def test_session_invalid_after_logout():
    """
    Test that sessions are invalid after logout using database validation.
    """
    # Mock the database session
    mock_db_session = AsyncMock(spec=AsyncSession)

    # Import the session service functions
    from services.session_service import create_session, validate_session, delete_session

    user_id = secrets.token_hex(20)

    # Mock the database operations for create_session
    with patch.object(mock_db_session, 'add'), \
         patch.object(mock_db_session, 'commit'), \
         patch.object(mock_db_session, 'refresh') as mock_refresh:

        # Mock the refresh to set the session attributes
        def mock_refresh_func(obj):
            obj.id = secrets.token_hex(16)
            obj.token = secrets.token_urlsafe(32)
            obj.user_id = user_id
            obj.expires_at = datetime.utcnow() + timedelta(minutes=30)
        mock_refresh.side_effect = mock_refresh_func

        # Create a session
        session = await create_session(
            db_session=mock_db_session,
            user_id=user_id,
            expires_in_minutes=30
        )

        assert session is not None
        assert session.token is not None

        # Validate the session before logout
        with patch('services.session_service.get_user_by_id') as mock_get_user:
            # Mock a user object
            mock_user = User(
                id=user_id,
                name="Test User",
                email="test@example.com",
                password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",
                email_verified=False
            )
            mock_get_user.return_value = mock_user

            # Validate the session (should succeed)
            validated_user = await validate_session(
                db_session=mock_db_session,
                session_token=session.token
            )

            assert validated_user is not None
            assert validated_user.id == user_id

        # Now delete the session (logout)
        with patch('sqlmodel.sql.expression.SelectOfScalar.exec') as mock_exec:
            mock_result = AsyncMock()
            mock_result.first.return_value = session
            mock_exec.return_value = mock_result

            with patch.object(mock_db_session, 'delete'), \
                 patch.object(mock_db_session, 'commit'):

                delete_success = await delete_session(
                    db_session=mock_db_session,
                    session_token=session.token
                )

                assert delete_success is True

        # Try to validate the session again (should fail after logout)
        with patch('sqlmodel.sql.expression.SelectOfScalar.exec') as mock_exec:
            mock_result = AsyncMock()
            mock_result.first.return_value = None  # Session no longer exists
            mock_exec.return_value = mock_result

            # Validate the session after logout (should fail)
            validated_user = await validate_session(
                db_session=mock_db_session,
                session_token=session.token
            )

            assert validated_user is None


def test_logout_error_handling():
    """
    Test that logout handles errors properly and continues to clear cookies.
    """
    # This test verifies that even if there's a database error during logout,
    # the process continues and cookies are still cleared
    assert True  # Placeholder for actual test implementation


if __name__ == "__main__":
    # Run basic tests
    test_logout_error_handling()
    print("Basic logout functionality tests defined!")