import pytest
from src.services.task_service import TaskService


class TestTaskService:
    def test_create_task(self):
        """Test creating a task."""
        service = TaskService()
        task = service.create_task("Test Title", "Test Description")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.status == "incomplete"

    def test_create_task_without_description(self):
        """Test creating a task without description."""
        service = TaskService()
        task = service.create_task("Test Title")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.status == "incomplete"

    def test_get_task_by_id(self):
        """Test getting a task by its ID."""
        service = TaskService()
        created_task = service.create_task("Test Title")

        retrieved_task = service.get_task_by_id(created_task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title

    def test_get_task_by_id_not_found(self):
        """Test getting a non-existent task."""
        service = TaskService()
        task = service.get_task_by_id(999)
        assert task is None

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        service = TaskService()
        task1 = service.create_task("Title 1")
        task2 = service.create_task("Title 2")

        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when none exist."""
        service = TaskService()
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 0

    def test_update_task_title(self):
        """Test updating a task's title."""
        service = TaskService()
        task = service.create_task("Original Title")

        updated_task = service.update_task(task.id, "New Title")
        assert updated_task is not None
        assert updated_task.title == "New Title"

    def test_update_task_description(self):
        """Test updating a task's description."""
        service = TaskService()
        task = service.create_task("Title", "Original Description")

        updated_task = service.update_task(task.id, description="New Description")
        assert updated_task is not None
        assert updated_task.description == "New Description"

    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        service = TaskService()
        task = service.create_task("Original Title", "Original Description")

        updated_task = service.update_task(task.id, "New Title", "New Description")
        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        service = TaskService()
        result = service.update_task(999, "New Title")
        assert result is None

    def test_toggle_status(self):
        """Test toggling task status."""
        service = TaskService()
        task = service.create_task("Title", status="incomplete")

        # Toggle from incomplete to complete
        toggled_task = service.toggle_status(task.id)
        assert toggled_task is not None
        assert toggled_task.status == "complete"

        # Toggle from complete to incomplete
        toggled_task = service.toggle_status(task.id)
        assert toggled_task is not None
        assert toggled_task.status == "incomplete"

    def test_toggle_status_not_found(self):
        """Test toggling status of a non-existent task."""
        service = TaskService()
        result = service.toggle_status(999)
        assert result is None

    def test_delete_task(self):
        """Test deleting a task."""
        service = TaskService()
        task = service.create_task("Title")

        # Verify task exists
        assert service.get_task_by_id(task.id) is not None

        # Delete the task
        result = service.delete_task(task.id)
        assert result is True

        # Verify task no longer exists
        assert service.get_task_by_id(task.id) is None

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        service = TaskService()
        result = service.delete_task(999)
        assert result is False

    def test_auto_incrementing_ids(self):
        """Test that IDs are auto-incrementing."""
        service = TaskService()
        task1 = service.create_task("Title 1")
        task2 = service.create_task("Title 2")
        task3 = service.create_task("Title 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_id_recycling_after_deletion(self):
        """Test that IDs are not recycled after deletion."""
        service = TaskService()
        task1 = service.create_task("Title 1")
        task2 = service.create_task("Title 2")

        # Delete the first task
        service.delete_task(task1.id)

        # Create a new task - it should get the next ID, not reuse the deleted one
        task3 = service.create_task("Title 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3  # Should be 3, not 1