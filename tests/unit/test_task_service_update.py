import pytest
from src.services.task_service import TaskService


class TestTaskServiceUpdate:
    def test_update_task_title(self):
        """Test updating a task's title."""
        service = TaskService()
        task = service.create_task("Original Title", "Original Description")

        result = service.update_task(task.id, "New Title")

        assert result is not None
        assert result.title == "New Title"
        assert result.description == "Original Description"  # Should remain unchanged

    def test_update_task_description(self):
        """Test updating a task's description."""
        service = TaskService()
        task = service.create_task("Original Title", "Original Description")

        result = service.update_task(task.id, description="New Description")

        assert result is not None
        assert result.title == "Original Title"  # Should remain unchanged
        assert result.description == "New Description"

    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        service = TaskService()
        task = service.create_task("Original Title", "Original Description")

        result = service.update_task(task.id, "New Title", "New Description")

        assert result is not None
        assert result.title == "New Title"
        assert result.description == "New Description"

    def test_update_task_nonexistent(self):
        """Test updating a non-existent task."""
        service = TaskService()

        result = service.update_task(999, "New Title")

        assert result is None

    def test_update_task_with_validation_error(self):
        """Test updating a task with invalid data."""
        service = TaskService()
        task = service.create_task("Original Title")

        # Try to update with an empty title (should fail validation)
        with pytest.raises(ValueError):
            service.update_task(task.id, "")  # Empty title should raise ValueError in the Task model