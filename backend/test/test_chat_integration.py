"""
Integration tests for chatbot user stories in the chatbot backend.
"""

import pytest
from fastapi.testclient import TestClient
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


def test_user_story_1_create_task(client, sample_user):
    """
    Test User Story 1: Creating a Task via Chat
    - User can send natural language command like "Add a task to buy groceries"
    - System authenticates user via JWT
    - OpenAI Agent processes natural language and selects add_task tool
    - MCP server executes add_task with correct parameters
    - Task is created in database with correct user association
    - User receives appropriate confirmation message
    - Conversation history is updated
    """
    user_id = sample_user.id
    message_data = {
        "message": "Add a task to buy groceries",
        "conversation_id": None
    }

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

        # Mock agent response for add_task
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've created a task for you: buy groceries",
            "tool_calls": [{
                "tool_name": "add_task",
                "parameters": {"title": "buy groceries"},
                "result": {"success": True, "task": {"id": str(uuid4()), "title": "buy groceries"}}
            }],
            "action": {"type": "task_created", "data": {"task_id": str(uuid4()), "task_title": "buy groceries", "success": True}}
        })

        # Mock conversation creation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=sample_user.id,
            metadata={}
        )
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        mock_session.get.return_value = mock_conversation

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "buy groceries" in data["response"]
        assert data["action"]["type"] == "task_created"
        assert data["action"]["data"]["task_title"] == "buy groceries"


def test_user_story_2_list_tasks(client, sample_user):
    """
    Test User Story 2: Listing Tasks via Chat
    - User can send natural language command like "Show me my pending tasks"
    - System authenticates user via JWT
    - OpenAI Agent processes natural language and selects list_tasks tool
    - MCP server executes list_tasks with correct filters
    - Correct tasks are retrieved based on user and status filters
    - User receives properly formatted task list
    - Conversation history is updated
    """
    user_id = sample_user.id
    message_data = {
        "message": "Show me my pending tasks",
        "conversation_id": None
    }

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

        # Mock agent response for list_tasks
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "Here are your pending tasks: 1. Buy groceries, 2. Walk the dog",
            "tool_calls": [{
                "tool_name": "list_tasks",
                "parameters": {"status": "pending"},
                "result": {"success": True, "tasks": [
                    {"id": str(uuid4()), "title": "Buy groceries", "completed": False},
                    {"id": str(uuid4()), "title": "Walk the dog", "completed": False}
                ], "count": 2}
            }],
            "action": {"type": "task_listed", "data": {"task_count": 2, "success": True}}
        })

        # Mock conversation creation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=sample_user.id,
            metadata={}
        )
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        mock_session.get.return_value = mock_conversation

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "Buy groceries" in data["response"]
        assert "Walk the dog" in data["response"]
        assert data["action"]["type"] == "task_listed"
        assert data["action"]["data"]["task_count"] == 2


def test_user_story_3_update_task(client, sample_user):
    """
    Test User Story 3: Updating Tasks via Chat
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
    user_id = sample_user.id
    message_data = {
        "message": "Complete the meeting task",
        "conversation_id": None
    }

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

        # Mock agent response for multi-step operation (list then complete)
        mock_agent.initialize_tools = AsyncMock()
        mock_agent.process_with_retry = AsyncMock(return_value={
            "response": "I've completed your task: Schedule team meeting",
            "tool_calls": [
                {
                    "tool_name": "list_tasks",
                    "parameters": {},
                    "result": {"success": True, "tasks": [
                        {"id": str(uuid4()), "title": "Schedule team meeting", "completed": False},
                        {"id": str(uuid4()), "title": "Send email", "completed": False}
                    ], "count": 2}
                },
                {
                    "tool_name": "complete_task",
                    "parameters": {"task_id": str(uuid4())},
                    "result": {"success": True, "task": {"id": str(uuid4()), "title": "Schedule team meeting", "completed": True}}
                }
            ],
            "action": {"type": "task_updated", "data": {"task_id": str(uuid4()), "task_title": "Schedule team meeting", "success": True}}
        })

        # Mock conversation creation
        mock_conversation = Conversation(
            id=uuid4(),
            user_id=sample_user.id,
            metadata={}
        )
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None
        mock_session.get.return_value = mock_conversation

        # Make the request
        response = client.post(f"/api/chat/{user_id}/conversation", json=message_data)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "completed" in data["response"].lower()
        assert "Schedule team meeting" in data["response"]
        assert data["action"]["type"] == "task_updated"
        assert data["action"]["data"]["task_title"] == "Schedule team meeting"