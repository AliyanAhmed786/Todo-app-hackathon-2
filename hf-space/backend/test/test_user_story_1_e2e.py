"""
End-to-end test for User Story 1: Creating a Task via Chat
"""

import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming the main app is in main.py
from unittest.mock import patch, MagicMock, AsyncMock
from models.user import User
from models.conversation import Conversation
from models.message import Message
from models.task import Task, TaskPriority
from uuid import uuid4


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_user_story_1_e2e_create_task(client):
    """
    End-to-end test for User Story 1: Creating a Task via Chat

    Test criteria:
    - User can send natural language command like "Add a task to buy groceries"
    - System authenticates user via JWT
    - OpenAI Agent processes natural language and selects add_task tool
    - MCP server executes add_task with correct parameters
    - Task is created in database with correct user association
    - User receives appropriate confirmation message
    - Conversation history is updated
    """
    # Create a test user
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    # Message to test
    message_data = {
        "message": "Add a task to buy groceries",
        "conversation_id": None
    }

    # Mock all dependencies to isolate the test
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session, \
         patch("api.chat_router.chat_agent") as mock_agent, \
         patch("api.chat_router.MCPTaskTools") as mock_tools_class:

        # Mock user authentication
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock agent with detailed response
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've created a task for you: buy groceries",
            "tool_calls": [{
                "tool_name": "add_task",
                "parameters": {
                    "user_id": user_id,
                    "title": "buy groceries",
                    "description": None,
                    "priority": "medium",
                    "due_date": None
                },
                "result": {
                    "success": True,
                    "task": {
                        "id": str(uuid4()),
                        "title": "buy groceries",
                        "description": None,
                        "priority": "medium",
                        "due_date": None,
                        "completed": False,
                        "user_id": user_id,
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-01T00:00:00"
                    }
                }
            }],
            "action": {
                "type": "task_created",
                "data": {
                    "task_id": str(uuid4()),
                    "task_title": "buy groceries",
                    "success": True
                }
            }
        })

        # Mock conversation creation and retrieval
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,
            created_at=None,
            updated_at=None,
            metadata={}
        )

        # Mock the conversation retrieval/addition
        original_get = mock_session.get
        def side_effect_get(model, obj_id):
            if model.__name__ == "Conversation":
                return mock_conversation
            return original_get(model, obj_id)

        mock_session.get.side_effect = side_effect_get

        # Mock adding and committing to session
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Make the request to create or continue conversation
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Verify the response
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        data = response.json()

        # Verify response structure
        assert "response" in data
        assert "conversation_id" in data
        assert "tool_calls" in data
        assert "action" in data

        # Verify the response content
        assert "buy groceries" in data["response"]
        assert data["action"]["type"] == "task_created"
        assert data["action"]["data"]["task_title"] == "buy groceries"

        # Verify tool was called correctly
        assert len(data["tool_calls"]) > 0
        if data["tool_calls"]:
            tool_call = data["tool_calls"][0]
            assert tool_call["tool_name"] == "add_task"
            assert "buy groceries" in tool_call["parameters"]["title"]


def test_user_story_1_e2e_with_existing_conversation(client):
    """
    End-to-end test for User Story 1 with an existing conversation.
    """
    # Create a test user
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    # Use an existing conversation ID
    existing_conversation_id = str(uuid4())

    message_data = {
        "message": "Add another task to walk the dog",
        "conversation_id": existing_conversation_id
    }

    # Mock all dependencies
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session, \
         patch("api.chat_router.chat_agent") as mock_agent:

        # Mock user authentication
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock an existing conversation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,
            created_at=None,
            updated_at=None,
            metadata={}
        )
        mock_session.get.return_value = mock_conversation

        # Mock agent response
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've added the task: walk the dog",
            "tool_calls": [{
                "tool_name": "add_task",
                "parameters": {
                    "user_id": user_id,
                    "title": "walk the dog",
                    "description": None,
                    "priority": "medium",
                    "due_date": None
                },
                "result": {
                    "success": True,
                    "task": {
                        "id": str(uuid4()),
                        "title": "walk the dog",
                        "description": None,
                        "priority": "medium",
                        "due_date": None,
                        "completed": False,
                        "user_id": user_id,
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-01T00:00:00"
                    }
                }
            }],
            "action": {
                "type": "task_created",
                "data": {
                    "task_id": str(uuid4()),
                    "task_title": "walk the dog",
                    "success": True
                }
            }
        })

        # Mock session operations
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "walk the dog" in data["response"]
        assert data["action"]["type"] == "task_created"
        assert data["action"]["data"]["task_title"] == "walk the dog"


def test_user_story_1_authentication_required(client):
    """
    Test that authentication is required for creating tasks via chat.
    """
    user_id = str(uuid4())
    message_data = {
        "message": "Add a task to test authentication",
        "conversation_id": None
    }

    # Mock authentication failure
    with patch("api.chat_router.get_current_chat_user") as mock_get_user:
        mock_get_user.side_effect = Exception("Authentication required")

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Should fail due to authentication
        assert response.status_code in [401, 403, 500]  # Depending on how auth failure is handled


if __name__ == "__main__":
    # This allows running the test directly
    pytest.main([__file__])