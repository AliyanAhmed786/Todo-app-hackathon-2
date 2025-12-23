import pytest
from src.services.task_service import TaskService


class TestTaskServiceDelete:
    def test_delete_task_success(self):
        """Test successfully deleting a task."""
        service = TaskService()
        task = service.create_task("Test Title")

        # Verify task exists
        assert service.get_task_by_id(task.id) is not None

        # Delete the task
        result = service.delete_task(task.id)

        # Verify result and that task no longer exists
        assert result is True
        assert service.get_task_by_id(task.id) is None

    def test_delete_task_nonexistent(self):
        """Test deleting a non-existent task."""
        service = TaskService()

        result = service.delete_task(999)

        assert result is False

    def test_delete_task_id_not_recycled(self):
        """Test that deleted task IDs are not recycled."""
        service = TaskService()
        task1 = service.create_task("Title 1")
        task2 = service.create_task("Title 2")

        # Delete the first task
        service.delete_task(task1.id)

        # Create a new task - it should get the next ID, not reuse the deleted one
        task3 = service.create_task("Title 3")

        # Verify IDs
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3  # Should be 3, not 1