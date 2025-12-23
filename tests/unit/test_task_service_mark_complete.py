import pytest
from src.services.task_service import TaskService


class TestTaskServiceMarkComplete:
    def test_toggle_status_incomplete_to_complete(self):
        """Test toggling status from incomplete to complete."""
        service = TaskService()
        task = service.create_task("Test Title", status="incomplete")

        result = service.toggle_status(task.id)

        assert result is not None
        assert result.status == "complete"

    def test_toggle_status_complete_to_incomplete(self):
        """Test toggling status from complete to incomplete."""
        service = TaskService()
        task = service.create_task("Test Title", status="complete")

        result = service.toggle_status(task.id)

        assert result is not None
        assert result.status == "incomplete"

    def test_toggle_status_nonexistent_task(self):
        """Test toggling status of a non-existent task."""
        service = TaskService()

        result = service.toggle_status(999)

        assert result is None

    def test_get_task_by_id_exists(self):
        """Test getting a task by ID that exists."""
        service = TaskService()
        created_task = service.create_task("Test Title")

        result = service.get_task_by_id(created_task.id)

        assert result is not None
        assert result.id == created_task.id
        assert result.title == created_task.title

    def test_get_task_by_id_not_exists(self):
        """Test getting a task by ID that doesn't exist."""
        service = TaskService()

        result = service.get_task_by_id(999)

        assert result is None