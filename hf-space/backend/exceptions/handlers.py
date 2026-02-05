from fastapi import Request, HTTPException, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError as SQLIntegrityError
from typing import Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TaskNotFoundError(HTTPException):
    """
    Exception raised when a task is not found.
    """
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            detail=f"Task with ID {task_id} not found"
        )

class UserNotFoundError(HTTPException):
    """
    Exception raised when a user is not found.
    """
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )

class UnauthorizedAccessError(HTTPException):
    """
    Exception raised when a user tries to access resources they don't own.
    """
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="You don't have permission to access this resource"
        )

class ValidationError(HTTPException):
    """
    Exception raised for validation errors.
    """
    def __init__(self, message: str):
        super().__init__(
            status_code=422,
            detail=message
        )

class DatabaseError(HTTPException):
    """
    Exception raised for database-related errors.
    """
    def __init__(self, message: str = "Database error occurred"):
        super().__init__(
            status_code=500,
            detail=message
        )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions.
    """
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle validation exceptions.
    """
    logger.error(f"Validation Exception: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "message": str(exc)}
    )

async def database_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle database exceptions.
    """
    logger.error(f"Database Exception: {str(exc)}")

    if isinstance(exc, SQLIntegrityError):
        return JSONResponse(
            status_code=400,
            content={"detail": "Database integrity error", "message": "A constraint violation occurred"}
        )

    return JSONResponse(
        status_code=500,
        content={"detail": "Database error", "message": "An error occurred while accessing the database"}
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions.
    """
    logger.error(f"General Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": "An unexpected error occurred"}
    )

def add_exception_handlers(app: FastAPI):
    """
    Add all exception handlers to the FastAPI application.
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)