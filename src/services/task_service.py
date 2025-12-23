from typing import List, Optional
from src.models.task import Task


class TaskService:
    def __init__(self):
        """
        Initialize the TaskService with in-memory storage.
        """
        self._tasks = {}  # Dictionary to store tasks by ID
        self._next_id = 1  # Auto-incrementing ID starting from 1

    def create_task(self, title: str, description: Optional[str] = None, status: str = "incomplete") -> Task:
        """
        Create a new task with the given title and optional description.

        Args:
            title: Title of the task (required, 1-200 characters, not only whitespace)
            description: Description of the task (optional, 0-1000 characters)
            status: Initial status of the task (optional, defaults to "incomplete")

        Returns:
            Task: The created task object
        """
        # Create the task with the next available ID
        task = Task(self._next_id, title, description, status)

        # Add task to storage
        self._tasks[self._next_id] = task

        # Increment the next ID for the next task
        self._next_id += 1

        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task: The task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List[Task]: List of all task objects
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update a task's title or description.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Task: Updated task object if successful, None if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        # Update title if provided
        if title is not None:
            task.update_title(title)

        # Update description if provided
        if description is not None:
            task.update_description(description)

        return task

    def toggle_status(self, task_id: int) -> Optional[Task]:
        """
        Toggle the status of a task between complete/incomplete.

        Args:
            task_id: ID of the task to toggle

        Returns:
            Task: Updated task object if successful, None if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.toggle_status()
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_next_available_id(self) -> int:
        """
        Get the next available ID for a new task.
        Note: This returns the next ID but doesn't guarantee it's available if IDs were deleted.
        The actual next ID used will be the smallest available positive integer.

        Returns:
            int: The next available ID
        """
        # Find the smallest positive integer not in use
        available_id = 1
        while available_id in self._tasks:
            available_id += 1
        return available_id

    def get_statistics(self):
        """
        Get statistics about tasks including total, completed, pending counts and completion rate.

        Returns:
            dict: Dictionary containing total_tasks, completed_tasks, pending_tasks, and completion_rate
        """
        all_tasks = self.get_all_tasks()
        total_tasks = len(all_tasks)

        completed_tasks = sum(1 for task in all_tasks if task.status == "complete")
        pending_tasks = total_tasks - completed_tasks

        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": completion_rate
        }