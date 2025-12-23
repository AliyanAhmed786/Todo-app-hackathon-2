from datetime import datetime
from typing import Optional


class Task:
    def __init__(self, task_id: int, title: str, description: Optional[str] = None, status: str = "incomplete"):
        """
        Initialize a Task instance.

        Args:
            task_id: Unique identifier for the task
            title: Title of the task (required, 1-200 characters, not only whitespace)
            description: Description of the task (optional, 0-1000 characters)
            status: Status of the task (either "incomplete" or "complete")
        """
        self.id = task_id
        self.title = self._validate_title(title)
        self.description = self._validate_description(description or "")
        self.status = self._validate_status(status)
        self.created_date = datetime.now()

    def _validate_title(self, title: str) -> str:
        """Validate title according to domain rules."""
        if not isinstance(title, str):
            raise ValueError("Title must be a string")

        if len(title) < 1 or len(title) > 200:
            raise ValueError("Title must be between 1-200 characters")

        if title.isspace() or title == "":
            raise ValueError("Title cannot be only whitespace characters")

        return title

    def _validate_description(self, description: str) -> str:
        """Validate description according to domain rules."""
        if not isinstance(description, str):
            raise ValueError("Description must be a string")

        if len(description) > 1000:
            raise ValueError("Description must be between 0-1000 characters")

        return description

    def _validate_status(self, status: str) -> str:
        """Validate status according to domain rules."""
        if status not in ["incomplete", "complete"]:
            raise ValueError("Status must be either 'incomplete' or 'complete'")

        return status

    def toggle_status(self):
        """Toggle the task status between complete/incomplete."""
        if self.status == "incomplete":
            self.status = "complete"
        else:
            self.status = "incomplete"

    def update_title(self, new_title: str):
        """Update the task title with validation."""
        self.title = self._validate_title(new_title)

    def update_description(self, new_description: str):
        """Update the task description with validation."""
        self.description = self._validate_description(new_description)

    def __str__(self):
        """String representation of the task."""
        return f"ID. {self.id} [{self.status}] {self.title} - {self.description}"