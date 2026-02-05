"""
Unit tests for MCP tools in the chatbot backend.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.tools import MCPTaskTools
from models.task import Task, TaskPriority
from sqlmodel import Session
from uuid import UUID
import uuid


@pytest.fixture
def mock_db_session():
    """Mock database session for testing."""
    session = MagicMock(spec=Session)
    return session


@pytest.fixture
def mock_task_service():
    """Mock task service for testing."""
    service = MagicMock()
    return service


@pytest.fixture
def mcp_tools(mock_db_session, mock_task_service):
    """Create MCP tools instance for testing."""
    tools = MCPTaskTools(mock_db_session)
    tools.task_service = mock_task_service
    return tools


@pytest.mark.asyncio
async def test_add_task_success(mcp_tools, mock_task_service):
    """Test successful task creation."""
    # Arrange
    user_id = str(uuid.uuid4())
    title = "Test Task"
    description = "Test Description"
    priority = "high"
    due_date = "2023-12-31"

    mock_task = Task(
        id=uuid.uuid4(),
        title=title,
        description=description,
        priority=TaskPriority.HIGH,
        user_id=user_id
    )
    mock_task_service.create_task.return_value = mock_task

    # Act
    result = await mcp_tools.add_task(user_id, title, description, priority, due_date)

    # Assert
    assert result["success"] is True
    assert result["task"]["title"] == title
    assert result["task"]["description"] == description
    assert result["task"]["priority"] == "high"
    mock_task_service.create_task.assert_called_once()


@pytest.mark.asyncio
async def test_add_task_invalid_priority(mcp_tools):
    """Test task creation with invalid priority."""
    # Act
    result = await mcp_tools.add_task("user123", "Test", "Desc", "invalid_priority")

    # Assert
    assert result["success"] is False
    assert "Invalid priority" in result["error"]


@pytest.mark.asyncio
async def test_list_tasks_success(mcp_tools, mock_db_session):
    """Test successful task listing."""
    # Arrange
    user_id = "user123"
    mock_tasks = [
        Task(
            id=uuid.uuid4(),
            title="Task 1",
            description="Desc 1",
            priority=TaskPriority.MEDIUM,
            user_id=user_id,
            completed=False
        )
    ]
    mock_db_session.exec.return_value.all.return_value = mock_tasks

    # Act
    result = await mcp_tools.list_tasks(user_id)

    # Assert
    assert result["success"] is True
    assert result["count"] == 1
    assert len(result["tasks"]) == 1


@pytest.mark.asyncio
async def test_complete_task_success(mcp_tools, mock_db_session):
    """Test successful task completion."""
    # Arrange
    user_id = "user123"
    task_id = str(uuid.uuid4())
    mock_task = Task(
        id=UUID(task_id),
        title="Test Task",
        description="Test Desc",
        priority=TaskPriority.MEDIUM,
        user_id=user_id,
        completed=False
    )
    mock_db_session.get.return_value = mock_task

    # Act
    result = await mcp_tools.complete_task(user_id, task_id)

    # Assert
    assert result["success"] is True
    assert result["task"]["completed"] is True
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_success(mcp_tools, mock_db_session):
    """Test successful task deletion."""
    # Arrange
    user_id = "user123"
    task_id = str(uuid.uuid4())
    mock_task = Task(
        id=UUID(task_id),
        title="Test Task",
        description="Test Desc",
        priority=TaskPriority.MEDIUM,
        user_id=user_id
    )
    mock_db_session.get.return_value = mock_task

    # Act
    result = await mcp_tools.delete_task(user_id, task_id)

    # Assert
    assert result["success"] is True
    assert result["message"] == "Task deleted successfully"
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_task_success(mcp_tools, mock_db_session):
    """Test successful task update."""
    # Arrange
    user_id = "user123"
    task_id = str(uuid.uuid4())
    new_title = "Updated Task"
    mock_task = Task(
        id=UUID(task_id),
        title="Old Task",
        description="Old Desc",
        priority=TaskPriority.MEDIUM,
        user_id=user_id,
        completed=False
    )
    mock_db_session.get.return_value = mock_task

    # Act
    result = await mcp_tools.update_task(user_id, task_id, title=new_title)

    # Assert
    assert result["success"] is True
    assert result["task"]["title"] == new_title
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()