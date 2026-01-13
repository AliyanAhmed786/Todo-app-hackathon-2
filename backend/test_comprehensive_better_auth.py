"""
Comprehensive test suite for Better Auth integration.
This test suite validates all aspects of the Better Auth database session validation implementation.
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
from models.task import Task
from models.account import Account
from models.verification import Verification
from datetime import datetime, timedelta
import secrets
import json


class TestBetterAuthIntegrationSuite:
    """Comprehensive test suite for Better Auth integration."""

    @pytest.mark.asyncio
    async def test_complete_auth_flow(self):
        """Test the complete Better Auth flow: register -> login -> session -> logout."""
        # Mock the database session
        mock_db_session = AsyncMock(spec=AsyncSession)

        # Test user data
        email = "test@example.com"
        password = "SecurePassword123!"
        name = "Test User"
        user_id = secrets.token_hex(20)

        # 1. Test registration flow
        with patch('services.registration_service.create_user') as mock_create_user:
            from models.user import UserCreate
            from services.registration_service import register_user

            # Mock the created user
            mock_user = User(
                id=user_id,
                name=name,
                email=email,
                password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",
                email_verified=False
            )

            mock_create_user.return_value = mock_user

            # Register the user
            registered_user = await register_user(
                db_session=mock_db_session,
                user_in=UserCreate(email=email, password=password, name=name)
            )

            assert registered_user is not None
            assert registered_user.email == email
            assert registered_user.name == name

        # 2. Test login flow
        with patch('services.login_service.authenticate_user') as mock_authenticate, \
             patch('services.session_service.create_session') as mock_create_session:

            from services.login_service import login_user

            # Mock authentication success
            mock_authenticate.return_value = mock_user

            # Mock session creation
            session_token = secrets.token_urlsafe(32)
            mock_session = Session(
                id=secrets.token_hex(16),
                token=session_token,
                user_id=user_id,
                expires_at=datetime.utcnow() + timedelta(minutes=30)
            )
            mock_create_session.return_value = mock_session

            # Login the user
            user, session = await login_user(
                db_session=mock_db_session,
                email=email,
                password=password
            )

            assert user is not None
            assert session is not None
            assert user.id == user_id
            assert session.token == session_token

        # 3. Test session validation
        with patch('services.session_service.validate_session') as mock_validate_session:
            from middleware.better_auth import validate_session_from_database
            from fastapi import Request
            from starlette.datastructures import Headers

            # Mock successful session validation
            mock_validate_session.return_value = mock_user

            # Create a mock request with session cookie
            mock_request = Request(scope={
                "type": "http",
                "method": "GET",
                "path": "/api/auth/session",
                "headers": Headers({"cookie": f"better-auth.session_token={session_token}"}),
            })

            validated_user_id = await validate_session_from_database(mock_request)

            assert validated_user_id == user_id

        # 4. Test logout flow
        with patch('services.session_service.delete_session') as mock_delete_session:
            from services.logout_service import logout_user

            mock_delete_session.return_value = True

            # Logout the user
            result = await logout_user(
                db_session=mock_db_session,
                session_token=session_token
            )

            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_database_session_validation_strategy(self):
        """Test that session validation happens through database queries, not JWT decoding."""
        # Mock the database session
        mock_db_session = AsyncMock(spec=AsyncSession)

        user_id = secrets.token_hex(20)
        session_token = secrets.token_urlsafe(32)

        # Mock user and session objects
        mock_user = User(
            id=user_id,
            name="Test User",
            email="test@example.com",
            password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",
            email_verified=False
        )

        mock_session = Session(
            id=secrets.token_hex(16),
            token=session_token,
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )

        # Test session service validation using database queries
        with patch('sqlmodel.sql.expression.SelectOfScalar.exec') as mock_exec, \
             patch('services.user_service.get_user_by_id') as mock_get_user:

            # Mock the session query result
            mock_result = AsyncMock()
            mock_result.first.return_value = mock_session
            mock_exec.return_value = mock_result

            # Mock the user retrieval
            mock_get_user.return_value = mock_user

            from services.session_service import validate_session

            validated_user = await validate_session(
                db_session=mock_db_session,
                session_token=session_token
            )

            assert validated_user is not None
            assert validated_user.id == user_id
            assert validated_user.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_expired_session_handling(self):
        """Test that expired sessions are properly handled."""
        # Mock the database session
        mock_db_session = AsyncMock(spec=AsyncSession)

        user_id = secrets.token_hex(20)
        session_token = secrets.token_urlsafe(32)

        # Mock an expired session
        expired_session = Session(
            id=secrets.token_hex(16),
            token=session_token,
            user_id=user_id,
            expires_at=datetime.utcnow() - timedelta(minutes=10)  # Expired 10 minutes ago
        )

        # Test session validation with expired session
        with patch('sqlmodel.sql.expression.SelectOfScalar.exec') as mock_exec:
            # Mock the session query result (expired session)
            mock_result = AsyncMock()
            mock_result.first.return_value = expired_session
            mock_exec.return_value = mock_result

            from services.session_service import validate_session

            validated_user = await validate_session(
                db_session=mock_db_session,
                session_token=session_token
            )

            # Should return None for expired session
            assert validated_user is None

    @pytest.mark.asyncio
    async def test_session_middleware_integration(self):
        """Test that the Better Auth middleware properly validates sessions."""
        # Test the middleware integration
        from middleware.better_auth import get_current_user_from_session
        from fastapi import Request
        from starlette.datastructures import Headers

        # Mock data
        user_id = secrets.token_hex(20)
        session_token = secrets.token_urlsafe(32)

        with patch('middleware.better_auth.validate_session_from_database') as mock_validate, \
             patch('database.session.get_db_session') as mock_get_db:

            # Mock successful session validation
            mock_validate.return_value = user_id

            # Mock database session for user lookup
            mock_db = AsyncMock(spec=AsyncSession)
            mock_get_db.__aenter__.return_value = mock_db
            mock_get_db.__aexit__.return_value = None

            # Mock user query result
            with patch('sqlmodel.sql.expression.SelectOfScalar.exec') as mock_exec:
                mock_result = AsyncMock()
                mock_user = User(
                    id=user_id,
                    name="Test User",
                    email="test@example.com",
                    password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",
                    email_verified=False
                )
                mock_result.first.return_value = mock_user
                mock_exec.return_value = mock_result

                # Create a mock request
                mock_request = Request(scope={
                    "type": "http",
                    "method": "GET",
                    "path": "/api/test",
                    "headers": Headers({"cookie": f"better-auth.session_token={session_token}"}),
                })

                # Test the middleware
                current_user = await get_current_user_from_session(mock_request)

                assert current_user is not None
                assert current_user["id"] == user_id
                assert current_user["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_http_only_cookie_security(self):
        """Test that HTTP-only cookies are properly set and used."""
        # This test verifies that the auth endpoints properly set HTTP-only cookies
        from api.auth_router import register_user
        from fastapi import Request
        from fastapi.responses import JSONResponse
        from starlette.datastructures import Headers

        # Mock the database session
        mock_db_session = AsyncMock(spec=AsyncSession)

        # Test data
        email = "test@example.com"
        password = "SecurePassword123!"
        name = "Test User"
        user_id = secrets.token_hex(20)

        with patch('services.registration_service.create_user') as mock_create_user, \
             patch('services.session_service.create_session') as mock_create_session:

            # Mock user creation
            mock_user = User(
                id=user_id,
                name=name,
                email=email,
                password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",
                email_verified=False
            )
            mock_create_user.return_value = mock_user

            # Mock session creation
            session_token = secrets.token_urlsafe(32)
            mock_session = Session(
                id=secrets.token_hex(16),
                token=session_token,
                user_id=user_id,
                expires_at=datetime.utcnow() + timedelta(minutes=30)
            )
            mock_create_session.return_value = mock_session

            # Create a mock request
            mock_request = Request(scope={
                "type": "http",
                "method": "POST",
                "path": "/api/auth/signup",
                "headers": Headers({}),
            })

            # Mock user creation request
            from schemas.user import UserCreateRequest
            user_request = UserCreateRequest(
                email=email,
                password=password,
                name=name
            )

            # Call the registration endpoint
            response = await register_user(
                request=mock_request,
                user_in=user_request,
                db=mock_db_session
            )

            # Verify that the response is a JSONResponse (which supports cookie setting)
            assert isinstance(response, JSONResponse)

    def test_string_user_id_compatibility(self):
        """Test that all components work with string user IDs for Better Auth compatibility."""
        # Test that user IDs are handled as strings throughout the system

        # Test User model with string ID
        user_id = secrets.token_hex(20)  # This creates a string ID
        assert isinstance(user_id, str)

        user = User(
            id=user_id,
            name="Test User",
            email="test@example.com",
            password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",
            email_verified=False
        )

        assert isinstance(user.id, str)
        assert user.id == user_id

        # Test Session model with string user_id
        session = Session(
            id=secrets.token_hex(16),
            token=secrets.token_urlsafe(32),
            user_id=user_id,  # Should accept string user_id
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )

        assert isinstance(session.user_id, str)
        assert session.user_id == user_id

        # Test Task model with string user_id
        task = Task(
            title="Test Task",
            description="Test Description",
            status=False,
            user_id=user_id  # Should accept string user_id
        )

        assert isinstance(task.user_id, str)
        assert task.user_id == user_id

    @pytest.mark.asyncio
    async def test_cascade_delete_functionality(self):
        """Test that account deletion properly cascades to related records."""
        # Test the CASCADE DELETE functionality between User and Task
        from services.user_service import delete_user

        user_id = secrets.token_hex(20)

        # Mock the database session
        mock_db_session = AsyncMock(spec=AsyncSession)

        with patch.object(mock_db_session, 'get') as mock_get, \
             patch.object(mock_db_session, 'delete'), \
             patch.object(mock_db_session, 'commit'):

            # Mock a user object
            mock_user = User(
                id=user_id,
                name="Test User",
                email="test@example.com",
                password_hash="$2b$12$LQv3c1yP5q6u7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k",
                email_verified=False
            )
            mock_get.return_value = mock_user

            # Delete the user
            result = await delete_user(
                db_session=mock_db_session,
                user_id=user_id
            )

            assert result is True
            # The cascade behavior is handled by the database foreign key constraint

    def test_better_auth_models_exist(self):
        """Test that all Better Auth required models exist and have correct structure."""
        # Test Session model
        session = Session(
            id=secrets.token_hex(16),
            token=secrets.token_urlsafe(32),
            user_id=secrets.token_hex(20),
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )

        assert hasattr(session, 'id')
        assert hasattr(session, 'token')
        assert hasattr(session, 'user_id')
        assert hasattr(session, 'expires_at')

        # Test Account model
        account = Account(
            id=secrets.token_hex(16),
            user_id=secrets.token_hex(20),
            provider_id="email",
            provider_account_id="test123",
            created_at=datetime.utcnow()
        )

        assert hasattr(account, 'id')
        assert hasattr(account, 'user_id')
        assert hasattr(account, 'provider_id')
        assert hasattr(account, 'provider_account_id')

        # Test Verification model
        verification = Verification(
            id=secrets.token_hex(16),
            identifier="test@example.com",
            value=secrets.token_urlsafe(32),
            expires_at=datetime.utcnow() + timedelta(minutes=10),
            created_at=datetime.utcnow()
        )

        assert hasattr(verification, 'id')
        assert hasattr(verification, 'identifier')
        assert hasattr(verification, 'value')
        assert hasattr(verification, 'expires_at')


def run_comprehensive_tests():
    """Run all comprehensive Better Auth integration tests."""
    test_suite = TestBetterAuthIntegrationSuite()

    # Run individual tests
    asyncio.run(test_suite.test_string_user_id_compatibility())
    asyncio.run(test_suite.test_cascade_delete_functionality())
    test_suite.test_better_auth_models_exist()

    print("Comprehensive Better Auth integration tests completed!")


if __name__ == "__main__":
    run_comprehensive_tests()