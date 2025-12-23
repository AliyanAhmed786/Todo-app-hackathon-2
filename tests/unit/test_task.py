import pytest
from datetime import datetime
from src.models.task import Task


class TestTaskModel:
    def test_create_task_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(1, "Test Title", "Test Description")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.status == "incomplete"
        assert isinstance(task.created_date, datetime)

    def test_create_task_with_minimal_data(self):
        """Test creating a task with minimal required data."""
        task = Task(1, "Test Title")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.status == "incomplete"

    def test_title_validation_min_length(self):
        """Test that title must be at least 1 character."""
        with pytest.raises(ValueError, match="Title must be between 1-200 characters"):
            Task(1, "")

    def test_title_validation_max_length(self):
        """Test that title must be at most 200 characters."""
        long_title = "a" * 201
        with pytest.raises(ValueError, match="Title must be between 1-200 characters"):
            Task(1, long_title)

    def test_title_validation_whitespace_only(self):
        """Test that title cannot be only whitespace."""
        with pytest.raises(ValueError, match="Title cannot be only whitespace characters"):
            Task(1, "   ")

        with pytest.raises(ValueError, match="Title cannot be only whitespace characters"):
            Task(1, "\t\n")

    def test_description_validation_max_length(self):
        """Test that description must be at most 1000 characters."""
        long_description = "a" * 1001
        with pytest.raises(ValueError, match="Description must be between 0-1000 characters"):
            Task(1, "Valid Title", long_description)

    def test_status_validation_valid_values(self):
        """Test that status can only be 'incomplete' or 'complete'."""
        task = Task(1, "Test Title", status="complete")
        assert task.status == "complete"

        task = Task(1, "Test Title", status="incomplete")
        assert task.status == "incomplete"

    def test_status_validation_invalid_value(self):
        """Test that invalid status values raise an error."""
        with pytest.raises(ValueError, match="Status must be either 'incomplete' or 'complete'"):
            Task(1, "Test Title", status="invalid")

    def test_toggle_status(self):
        """Test toggling task status."""
        task = Task(1, "Test Title", status="incomplete")
        assert task.status == "incomplete"

        task.toggle_status()
        assert task.status == "complete"

        task.toggle_status()
        assert task.status == "incomplete"

    def test_update_title(self):
        """Test updating task title with validation."""
        task = Task(1, "Original Title")
        assert task.title == "Original Title"

        task.update_title("New Title")
        assert task.title == "New Title"

    def test_update_title_validation(self):
        """Test that updating title validates the new title."""
        task = Task(1, "Original Title")

        with pytest.raises(ValueError):
            task.update_title("")  # Empty title

        with pytest.raises(ValueError):
            task.update_title("   ")  # Whitespace only

        with pytest.raises(ValueError):
            task.update_title("a" * 201)  # Too long

    def test_update_description(self):
        """Test updating task description with validation."""
        task = Task(1, "Test Title", "Original Description")
        assert task.description == "Original Description"

        task.update_description("New Description")
        assert task.description == "New Description"

    def test_update_description_validation(self):
        """Test that updating description validates the new description."""
        task = Task(1, "Test Title", "Original Description")

        with pytest.raises(ValueError):
            task.update_description("a" * 1001)  # Too long