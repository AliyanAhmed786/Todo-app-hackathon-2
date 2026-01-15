"""
Chat-specific exceptions for chatbot backend.
"""

from fastapi import HTTPException, status


class ChatException(Exception):
    """Base exception class for chat-related errors."""
    pass


class InvalidTaskReferenceException(ChatException):
    """Raised when a user refers to a task that doesn't exist."""

    def __init__(self, message: str = "Task not found. Please clarify or list your tasks."):
        self.message = message
        super().__init__(self.message)


class UserTaskAccessException(ChatException):
    """Raised when a user tries to access a task they don't own."""

    def __init__(self, message: str = "Access denied: You don't have permission to access this task."):
        self.message = message
        super().__init__(self.message)


class DatabaseOperationException(ChatException):
    """Raised when database operations fail."""

    def __init__(self, message: str = "Database operation failed. Please try again."):
        self.message = message
        super().__init__(self.message)


class AIServiceUnavailableException(ChatException):
    """Raised when the AI service is unavailable."""

    def __init__(self, message: str = "AI service temporarily unavailable. Please try again."):
        self.message = message
        super().__init__(self.message)


class InvalidTokenException(ChatException):
    """Raised when JWT token is invalid or expired."""

    def __init__(self, message: str = "Invalid or expired token. Please log in again."):
        self.message = message
        super().__init__(self.message)


class UserIdMismatchException(ChatException):
    """Raised when user_id in path doesn't match JWT token subject."""

    def __init__(self, message: str = "User ID mismatch. Access denied."):
        self.message = message
        super().__init__(self.message)


def create_invalid_task_reference_http_exception():
    """Create an HTTPException for invalid task reference."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found. Please clarify or list your tasks."
    )


def create_user_task_access_http_exception():
    """Create an HTTPException for user task access violation."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied: You don't have permission to access this task."
    )


def create_database_operation_http_exception():
    """Create an HTTPException for database operation failures."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database operation failed. Please try again."
    )


def create_ai_service_unavailable_http_exception():
    """Create an HTTPException for AI service unavailability."""
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="AI service temporarily unavailable. Please try again."
    )


def create_invalid_token_http_exception():
    """Create an HTTPException for invalid JWT token."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again."
    )


def create_user_id_mismatch_http_exception():
    """Create an HTTPException for user ID mismatch."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User ID mismatch. Access denied."
    )