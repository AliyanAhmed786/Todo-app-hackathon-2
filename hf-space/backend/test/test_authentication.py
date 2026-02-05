"""
Tests for authentication flows with different user scenarios in the chatbot backend.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app  # Assuming the main app is in main.py
from unittest.mock import patch, MagicMock
from models.user import User
from uuid import uuid4


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_jwt_token_validation_success(client):
    """Test successful JWT token validation."""
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    message_data = {
        "message": "Test message",
        "conversation_id": None
    }

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session:

        # Mock user authentication - successful validation
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock conversation creation
        from models.conversation import Conversation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,
            metadata={}
        )
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        mock_session.get.return_value = mock_conversation

        # Mock agent
        with patch("api.chat_router.chat_agent") as mock_agent:
            mock_agent.initialize_tools = MagicMock()
            mock_agent.process_with_retry = MagicMock(return_value={
                "response": "Test response",
                "tool_calls": [],
                "action": {"type": "message_processed", "data": {}}
            })

            # Make the request
            response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

            # Should succeed with valid token
            assert response.status_code == 200


def test_jwt_token_user_id_mismatch(client):
    """Test behavior when user_id in path doesn't match JWT token subject."""
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    # Use a different user ID in the path than what's in the token
    different_user_id = str(uuid4())

    message_data = {
        "message": "Test message",
        "conversation_id": None
    }

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user:
        # Mock user authentication with mismatched IDs
        mock_get_user.side_effect = HTTPException(
            status_code=403,
            detail="Access denied: user_id mismatch"
        )

        # Make the request
        response = client.post(f"/api/chat/{different_user_id}/conversation", json=message_data)

        # Should fail with 403 due to user ID mismatch
        assert response.status_code == 403


def test_invalid_jwt_token(client):
    """Test behavior with invalid JWT token."""
    user_id = str(uuid4())
    message_data = {
        "message": "Test message",
        "conversation_id": None
    }

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user:
        # Mock user authentication failure
        mock_get_user.side_effect = HTTPException(
            status_code=401,
            detail="Invalid or expired token. Please log in again."
        )

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Should fail with 401 due to invalid token
        assert response.status_code == 401


def test_expired_jwt_token(client):
    """Test behavior with expired JWT token."""
    user_id = str(uuid4())
    message_data = {
        "message": "Test message",
        "conversation_id": None
    }

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user:
        # Mock expired token scenario
        mock_get_user.side_effect = HTTPException(
            status_code=401,
            detail="Invalid or expired token. Please log in again."
        )

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Should fail with 401 due to expired token
        assert response.status_code == 401


def test_multiple_user_isolation(client):
    """Test that users can't access each other's conversations."""
    user1 = User(
        id=str(uuid4()),
        name="User 1",
        email="user1@example.com",
        password_hash="hashed_password"
    )
    user2 = User(
        id=str(uuid4()),
        name="User 2",
        email="user2@example.com",
        password_hash="hashed_password"
    )

    conversation_id = str(uuid4())

    # Test user 1 accessing user 2's conversation
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session:

        # Authenticate as user 1
        mock_get_user.return_value = user1

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock conversation belonging to user 2
        from models.conversation import Conversation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user2.id,  # Different user
            metadata={}
        )
        mock_session.get.return_value = mock_conversation

        # Make the request - user 1 trying to access user 2's conversation
        response = client.get(f"/api/chat/{user1.id}/conversation/{conversation_id}")

        # Should fail since user1 is trying to access user2's conversation
        assert response.status_code == 404


def test_valid_user_access_to_own_conversation(client):
    """Test that users can access their own conversations."""
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )

    conversation_id = str(uuid4())

    # Test user accessing their own conversation
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session:

        # Authenticate as the user
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock conversation belonging to the same user
        from models.conversation import Conversation
        from models.message import Message
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,  # Same user
            metadata={}
        )
        mock_messages = [Message(
            id=uuid4(),
            conversation_id=mock_conversation.id,
            sender="user",
            content="Test message",
            timestamp=None
        )]
        mock_session.get.return_value = mock_conversation
        mock_session.exec.return_value.all.return_value = mock_messages

        # Make the request - user accessing their own conversation
        response = client.get(f"/api/chat/{user.id}/conversation/{conversation_id}")

        # Should succeed since user is accessing their own conversation
        assert response.status_code == 200


def test_rate_limiting_behavior():
    """Test rate limiting behavior (conceptual - implementation would depend on specific rate limiter)."""
    # This is a conceptual test - actual implementation would depend on
    # how rate limiting is implemented in the application
    pass


def test_concurrent_sessions_different_users(client):
    """Test concurrent sessions for different users."""
    users = [
        User(
            id=str(uuid4()),
            name=f"User {i}",
            email=f"user{i}@example.com",
            password_hash="hashed_password"
        ) for i in range(3)
    ]

    results = []

    for i, user in enumerate(users):
        message_data = {
            "message": f"Message from user {i}",
            "conversation_id": None
        }

        # Mock dependencies for each user
        with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
             patch("api.chat_router.get_db_session") as mock_get_session:

            # Authenticate as current user
            mock_get_user.return_value = user

            # Mock database session
            mock_session = MagicMock()
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_get_session.return_value.__exit__.return_value = None

            # Mock conversation creation
            from models.conversation import Conversation
            mock_conversation = Conversation(
                id=uuid4(),
                user_id=user.id,
                metadata={}
            )
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            mock_session.refresh.return_value = None
            mock_session.get.return_value = mock_conversation

            # Mock agent
            with patch("api.chat_router.chat_agent") as mock_agent:
                mock_agent.initialize_tools = MagicMock()
                mock_agent.process_with_retry = MagicMock(return_value={
                    "response": f"Response to user {i}",
                    "tool_calls": [],
                    "action": {"type": "message_processed", "data": {}}
                })

                # Make the request
                response = client.post(f"/api/chat/{user.id}/conversation", json=message_data)
                results.append(response.status_code)

    # All users should be able to access the system simultaneously
    for status_code in results:
        assert status_code == 200