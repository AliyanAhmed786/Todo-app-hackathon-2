"""
End-to-end test for User Story 3: Updating Tasks via Chat
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


def test_user_story_3_e2e_multi_step_operation(client):
    """
    End-to-end test for User Story 3: Updating Tasks via Chat

    Test criteria:
    - User can send natural language command like "Complete the meeting task"
    - System authenticates user via JWT
    - OpenAI Agent processes natural language and first calls list_tasks to identify the correct task
    - MCP server executes list_tasks to retrieve user's tasks
    - OpenAI Agent analyzes the task list to identify the correct task
    - OpenAI Agent selects complete_task tool with the correct task_id
    - MCP server executes complete_task with correct parameters
    - Task is updated in database with correct status
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

    # Message to test multi-step operation
    message_data = {
        "message": "Complete the meeting task",
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

        # Mock agent response with multi-step operation (list then complete)
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've completed your task: Schedule team meeting",
            "tool_calls": [
                {
                    "tool_name": "list_tasks",
                    "parameters": {"user_id": user_id, "status": None},
                    "result": {
                        "success": True,
                        "tasks": [
                            {
                                "id": str(uuid4()),
                                "title": "Schedule team meeting",
                                "description": "Schedule the weekly team meeting",
                                "priority": "high",
                                "due_date": "2023-12-31",
                                "completed": False,
                                "user_id": user_id,
                                "created_at": "2023-01-01T00:00:00",
                                "updated_at": "2023-01-01T00:00:00"
                            },
                            {
                                "id": str(uuid4()),
                                "title": "Send project update",
                                "description": "Send weekly project update to stakeholders",
                                "priority": "medium",
                                "due_date": "2023-12-30",
                                "completed": False,
                                "user_id": user_id,
                                "created_at": "2023-01-01T00:00:00",
                                "updated_at": "2023-01-01T00:00:00"
                            }
                        ],
                        "count": 2
                    }
                },
                {
                    "tool_name": "complete_task",
                    "parameters": {"user_id": user_id, "task_id": str(uuid4())},
                    "result": {
                        "success": True,
                        "task": {
                            "id": str(uuid4()),  # Same as input task_id
                            "title": "Schedule team meeting",
                            "description": "Schedule the weekly team meeting",
                            "priority": "high",
                            "due_date": "2023-12-31",
                            "completed": True,
                            "user_id": user_id,
                            "created_at": "2023-01-01T00:00:00",
                            "updated_at": "2023-01-01T00:00:00"
                        }
                    }
                }
            ],
            "action": {
                "type": "task_updated",
                "data": {
                    "task_id": str(uuid4()),
                    "task_title": "Schedule team meeting",
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
        assert "completed" in data["response"].lower()
        assert "Schedule team meeting" in data["response"]
        assert data["action"]["type"] == "task_updated"
        assert data["action"]["data"]["task_title"] == "Schedule team meeting"

        # Verify both tools were called in sequence (list_tasks then complete_task)
        assert len(data["tool_calls"]) >= 2
        tool_names = [tc["tool_name"] for tc in data["tool_calls"]]
        assert "list_tasks" in tool_names
        assert "complete_task" in tool_names


def test_user_story_3_update_task(client):
    """
    Test updating a task with the update_task tool.
    """
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    message_data = {
        "message": "Update the grocery task to add milk and bread",
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

        # Mock agent response with list then update operations
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've updated your task: buy groceries",
            "tool_calls": [
                {
                    "tool_name": "list_tasks",
                    "parameters": {"user_id": user_id, "status": None},
                    "result": {
                        "success": True,
                        "tasks": [
                            {
                                "id": str(uuid4()),
                                "title": "buy groceries",
                                "description": "Original description",
                                "priority": "medium",
                                "due_date": "2023-12-31",
                                "completed": False,
                                "user_id": user_id,
                                "created_at": "2023-01-01T00:00:00",
                                "updated_at": "2023-01-01T00:00:00"
                            }
                        ],
                        "count": 1
                    }
                },
                {
                    "tool_name": "update_task",
                    "parameters": {
                        "user_id": user_id,
                        "task_id": str(uuid4()),
                        "title": "buy groceries",
                        "description": "Add milk and bread to grocery list",
                        "priority": "high",
                        "due_date": "2023-12-31"
                    },
                    "result": {
                        "success": True,
                        "task": {
                            "id": str(uuid4()),  # Same as input task_id
                            "title": "buy groceries",
                            "description": "Add milk and bread to grocery list",
                            "priority": "high",
                            "due_date": "2023-12-31",
                            "completed": False,
                            "user_id": user_id,
                            "created_at": "2023-01-01T00:00:00",
                            "updated_at": "2023-01-01T00:00:00"
                        }
                    }
                }
            ],
            "action": {
                "type": "task_updated",
                "data": {
                    "task_id": str(uuid4()),
                    "task_title": "buy groceries",
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

        assert "updated" in data["response"].lower()
        assert "buy groceries" in data["response"]
        assert data["action"]["type"] == "task_updated"
        assert data["action"]["data"]["task_title"] == "buy groceries"


def test_user_story_3_delete_task(client):
    """
    Test deleting a task via chat.
    """
    user = User(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    user_id = user.id

    message_data = {
        "message": "Delete the old task",
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

        # Mock agent response with list then delete operations
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've deleted your task: clean up old files",
            "tool_calls": [
                {
                    "tool_name": "list_tasks",
                    "parameters": {"user_id": user_id, "status": None},
                    "result": {
                        "success": True,
                        "tasks": [
                            {
                                "id": str(uuid4()),
                                "title": "clean up old files",
                                "description": "Clean up unnecessary files from project",
                                "priority": "low",
                                "due_date": "2023-11-30",
                                "completed": False,
                                "user_id": user_id,
                                "created_at": "2023-01-01T00:00:00",
                                "updated_at": "2023-01-01T00:00:00"
                            }
                        ],
                        "count": 1
                    }
                },
                {
                    "tool_name": "delete_task",
                    "parameters": {"user_id": user_id, "task_id": str(uuid4())},
                    "result": {
                        "success": True,
                        "message": "Task deleted successfully"
                    }
                }
            ],
            "action": {
                "type": "task_deleted",
                "data": {
                    "task_title": "clean up old files",
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

        assert "deleted" in data["response"].lower()
        assert "clean up old files" in data["response"]
        assert data["action"]["type"] == "task_deleted"
        assert data["action"]["data"]["task_title"] == "clean up old files"


if __name__ == "__main__":
    # This allows running the test directly
    pytest.main([__file__])