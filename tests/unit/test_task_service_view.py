import pytest
from src.services.task_service import TaskService


class TestTaskServiceView:
    def test_get_all_tasks_empty(self):
        """Test getting all tasks when none exist."""
        service = TaskService()
        tasks = service.get_all_tasks()

        assert len(tasks) == 0

    def test_get_all_tasks_single_task(self):
        """Test getting all tasks with a single task."""
        service = TaskService()
        task = service.create_task("Test Title")
        tasks = service.get_all_tasks()

        assert len(tasks) == 1
        assert tasks[0].id == task.id
        assert tasks[0].title == task.title

    def test_get_all_tasks_multiple_tasks(self):
        """Test getting all tasks with multiple tasks."""
        service = TaskService()
        task1 = service.create_task("Title 1")
        task2 = service.create_task("Title 2")
        task3 = service.create_task("Title 3")

        tasks = service.get_all_tasks()

        assert len(tasks) == 3
        task_ids = [task.id for task in tasks]
        assert task1.id in task_ids
        assert task2.id in task_ids
        assert task3.id in task_ids

    def test_get_task_by_id_exists(self):
        """Test getting a task by ID that exists."""
        service = TaskService()
        created_task = service.create_task("Test Title")

        retrieved_task = service.get_task_by_id(created_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title

    def test_get_task_by_id_not_exists(self):
        """Test getting a task by ID that doesn't exist."""
        service = TaskService()

        retrieved_task = service.get_task_by_id(999)

        assert retrieved_task is None