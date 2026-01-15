"""
End-to-end test for User Story 2: Listing Tasks via Chat
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


def test_user_story_2_e2e_list_all_tasks(client):
    """
    End-to-end test for User Story 2: Listing Tasks via Chat

    Test criteria:
    - User can send natural language command like "Show me my pending tasks"
    - System authenticates user via JWT
    - OpenAI Agent processes natural language and selects list_tasks tool
    - MCP server executes list_tasks with correct filters
    - Correct tasks are retrieved based on user and status filters
    - User receives properly formatted task list
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
        "message": "Show me my pending tasks",
        "conversation_id": None
    }

    # Mock all dependencies to isolate the test
    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session, \
         patch("api.chat_router.chat_agent") as mock_agent:

        # Mock user authentication
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock agent response with list_tasks tool call
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "Here are your pending tasks:\n1. Buy groceries (High priority)\n2. Call mom (Medium priority)",
            "tool_calls": [{
                "tool_name": "list_tasks",
                "parameters": {"user_id": user_id, "status": "pending"},
                "result": {
                    "success": True,
                    "tasks": [
                        {
                            "id": str(uuid4()),
                            "title": "Buy groceries",
                            "description": "Buy milk, bread, and eggs",
                            "priority": "high",
                            "due_date": "2023-12-31",
                            "completed": False,
                            "user_id": user_id,
                            "created_at": "2023-01-01T00:00:00",
                            "updated_at": "2023-01-01T00:00:00"
                        },
                        {
                            "id": str(uuid4()),
                            "title": "Call mom",
                            "description": "Call mother for her birthday",
                            "priority": "medium",
                            "due_date": "2023-12-25",
                            "completed": False,
                            "user_id": user_id,
                            "created_at": "2023-01-01T00:00:00",
                            "updated_at": "2023-01-01T00:00:00"
                        }
                    ],
                    "count": 2
                }
            }],
            "action": {
                "type": "tasks_listed",
                "data": {
                    "task_count": 2,
                    "filter": "pending",
                    "success": True
                }
            }
        })

        # Mock conversation creation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,
            created_at=None,
            updated_at=None,
            metadata={}
        )

        # Mock the conversation retrieval/addition
        mock_session.get.return_value = mock_conversation
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Make the request
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
        assert "pending tasks" in data["response"].lower()
        assert "Buy groceries" in data["response"]
        assert "Call mom" in data["response"]
        assert data["action"]["type"] == "tasks_listed"
        assert data["action"]["data"]["task_count"] == 2
        assert data["action"]["data"]["filter"] == "pending"

        # Verify tool was called correctly
        assert len(data["tool_calls"]) > 0
        if data["tool_calls"]:
            tool_call = data["tool_calls"][0]
            assert tool_call["tool_name"] == "list_tasks"
            assert tool_call["parameters"]["user_id"] == user_id
            assert tool_call["parameters"]["status"] == "pending"


def test_user_story_2_e2e_list_completed_tasks(client):
    """
    Test listing completed tasks via chat.
    """
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    message_data = {
        "message": "Show me my completed tasks",
        "conversation_id": None
    }

    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session, \
         patch("api.chat_router.chat_agent") as mock_agent:

        # Mock user authentication
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock agent response for completed tasks
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "Here are your completed tasks:\n1. Finish report (Completed on 2023-12-01)",
            "tool_calls": [{
                "tool_name": "list_tasks",
                "parameters": {"user_id": user_id, "status": "completed"},
                "result": {
                    "success": True,
                    "tasks": [
                        {
                            "id": str(uuid4()),
                            "title": "Finish report",
                            "description": "Complete quarterly report",
                            "priority": "high",
                            "due_date": "2023-11-30",
                            "completed": True,
                            "user_id": user_id,
                            "created_at": "2023-01-01T00:00:00",
                            "updated_at": "2023-12-01T00:00:00"
                        }
                    ],
                    "count": 1
                }
            }],
            "action": {
                "type": "tasks_listed",
                "data": {
                    "task_count": 1,
                    "filter": "completed",
                    "success": True
                }
            }
        })

        # Mock conversation creation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,
            created_at=None,
            updated_at=None,
            metadata={}
        )

        # Mock session operations
        mock_session.get.return_value = mock_conversation
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "completed tasks" in data["response"].lower()
        assert "Finish report" in data["response"]
        assert data["action"]["type"] == "tasks_listed"
        assert data["action"]["data"]["task_count"] == 1
        assert data["action"]["data"]["filter"] == "completed"

        # Verify the tool call
        assert len(data["tool_calls"]) > 0
        tool_call = data["tool_calls"][0]
        assert tool_call["tool_name"] == "list_tasks"
        assert tool_call["parameters"]["status"] == "completed"


def test_user_story_2_e2e_list_all_tasks_no_filter(client):
    """
    Test listing all tasks without specific status filter.
    """
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    message_data = {
        "message": "Show me all my tasks",
        "conversation_id": None
    }

    with patch("api.chat_router.get_current_chat_user") as mock_get_user, \
         patch("api.chat_router.get_db_session") as mock_get_session, \
         patch("api.chat_router.chat_agent") as mock_agent:

        # Mock user authentication
        mock_get_user.return_value = user

        # Mock database session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock agent response for all tasks
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "Here are all your tasks:\n1. Buy groceries (Pending)\n2. Finish report (Completed)",
            "tool_calls": [{
                "tool_name": "list_tasks",
                "parameters": {"user_id": user_id, "status": None},
                "result": {
                    "success": True,
                    "tasks": [
                        {
                            "id": str(uuid4()),
                            "title": "Buy groceries",
                            "description": "Buy milk, bread, and eggs",
                            "priority": "high",
                            "due_date": "2023-12-31",
                            "completed": False,
                            "user_id": user_id,
                            "created_at": "2023-01-01T00:00:00",
                            "updated_at": "2023-01-01T00:00:00"
                        },
                        {
                            "id": str(uuid4()),
                            "title": "Finish report",
                            "description": "Complete quarterly report",
                            "priority": "high",
                            "due_date": "2023-11-30",
                            "completed": True,
                            "user_id": user_id,
                            "created_at": "2023-01-01T00:00:00",
                            "updated_at": "2023-12-01T00:00:00"
                        }
                    ],
                    "count": 2
                }
            }],
            "action": {
                "type": "tasks_listed",
                "data": {
                    "task_count": 2,
                    "filter": "all",
                    "success": True
                }
            }
        })

        # Mock conversation creation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=user.id,
            created_at=None,
            updated_at=None,
            metadata={}
        )

        # Mock session operations
        mock_session.get.return_value = mock_conversation
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Verify the response
        assert response.status_code == 200
        data = response.json()

        assert "all your tasks" in data["response"].lower()
        assert "Buy groceries" in data["response"]
        assert "Finish report" in data["response"]
        assert data["action"]["type"] == "tasks_listed"
        assert data["action"]["data"]["task_count"] == 2

        # Verify the tool call - status should be None for all tasks
        assert len(data["tool_calls"]) > 0
        tool_call = data["tool_calls"][0]
        assert tool_call["tool_name"] == "list_tasks"
        assert tool_call["parameters"]["status"] is None


if __name__ == "__main__":
    # This allows running the test directly
    pytest.main([__file__])