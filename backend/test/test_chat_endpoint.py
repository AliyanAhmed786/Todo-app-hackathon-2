"""
Unit tests for chat endpoint in the chatbot backend.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app  # Assuming the main app is in main.py
from unittest.mock import patch, MagicMock, AsyncMock
from models.user import User
from models.conversation import Conversation
from models.message import Message
from uuid import uuid4
import json


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )


@pytest.mark.parametrize("message_data,expected_status", [
    ({"message": "Add a task to buy groceries"}, 200),
    ({"message": "", "conversation_id": None}, 400),  # Empty message
    ({"message": "Test message", "conversation_id": "invalid-uuid"}, 400),  # Invalid UUID
])
def test_create_or_continue_conversation(client, sample_user, message_data, expected_status):
    """Test creating or continuing a conversation."""
    user_id = sample_user.id

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session, \
         patch("api.chat_router.chat_agent") as mock_agent:

        # Mock user authentication
        mock_get_user.return_value = sample_user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock agent response
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "Test response",
            "tool_calls": [],
            "action": {"type": "test", "data": {}}
        })

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        assert response.status_code == expected_status


def test_get_conversation_history(client, sample_user):
    """Test getting conversation history."""
    user_id = sample_user.id
    conversation_id = str(uuid4())

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session:

        # Mock user authentication
        mock_get_user.return_value = sample_user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock conversation and messages
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=sample_user.id,
            metadata={}
        )
        mock_messages = [
            Message(
                id=uuid4(),
                conversation_id=mock_conversation.id,
                sender="user",
                content="Hello",
                timestamp=None
            )
        ]

        mock_session.get.return_value = mock_conversation
        mock_session.exec.return_value.all.return_value = mock_messages

        # Make the request
        response = client.get(f"/api/chat/{user_id}/conversation/{conversation_id}")

        assert response.status_code == 200
        data = response.json()
        assert "messages" in data


def test_delete_conversation(client, sample_user):
    """Test deleting a conversation."""
    user_id = sample_user.id
    conversation_id = str(uuid4())

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session:

        # Mock user authentication
        mock_get_user.return_value = sample_user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock conversation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=sample_user.id,
            metadata={}
        )
        mock_session.get.return_value = mock_conversation

        # Make the request
        response = client.delete(f"/api/chat/{user_id}/conversation/{conversation_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


def test_invalid_conversation_id_format(client, sample_user):
    """Test handling of invalid conversation ID format."""
    user_id = sample_user.id
    invalid_conversation_id = "not-a-valid-uuid"

    # Mock dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user:
        # Mock user authentication
        mock_get_user.return_value = sample_user

        # Make the request
        response = client.get(f"/api/chat/{user_id}/conversation/{invalid_conversation_id}")

        assert response.status_code == 400
        data = response.json()
        assert "Invalid conversation_id format" in data["detail"]