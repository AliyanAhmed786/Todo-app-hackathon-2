from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import datetime
from enum import Enum

class PriorityEnum(int, Enum):
    """
    Enum for task priority levels.
    """
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TaskCreateRequest(BaseModel):
    """
    Schema for creating a new task.
    """
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[int] = 2  # Default to medium (2)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or len(v) < 1:
            raise ValueError('Title must be at least 1 character long')
        if len(v) > 200:
            raise ValueError('Title must be no more than 200 characters')
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be no more than 1000 characters')
        return v

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v and len(v) > 100:
            raise ValueError('Category must be no more than 100 characters')
        return v

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v is None:
            return 2  # Default to medium (2)
        return PriorityValue.validate(v)

class PriorityValue:
    """Custom validator to handle both string and integer priority values"""
    @classmethod
    def validate(cls, v):
        if v is not None:
            # Handle string to integer mapping for compatibility
            if isinstance(v, str):
                priority_map = {
                    'High': 3, 'high': 3, 'HIGH': 3,
                    'Medium': 2, 'medium': 2, 'MEDIUM': 2,
                    'Low': 1, 'low': 1, 'LOW': 1,
                    '3': 3, '2': 2, '1': 1
                }
                if v in priority_map:
                    return priority_map[v]
                try:
                    return int(v)
                except ValueError:
                    raise ValueError('Priority must be "High", "Medium", "Low" or 1, 2, 3')
            elif isinstance(v, int):
                if v not in [1, 2, 3]:
                    raise ValueError('Priority must be 1 (Low), 2 (Medium), or 3 (High)')
                return v
            else:
                try:
                    return int(v)
                except (ValueError, TypeError):
                    raise ValueError('Priority must be "High", "Medium", "Low" or 1, 2, 3')
        return v


from typing import Any

class TaskUpdateRequest(BaseModel):
    """
    Schema for updating a task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Any] = None  # Flexible Boolean: Allow Any type for smart validator to handle
    category: Optional[str] = None
    priority: Optional[Any] = None  # Sync Priority Type: Allow Any type for smart validator to handle
    due_date: Optional[str] = None

    class Config:
        extra = 'ignore'  # Ignore extra fields like id, created_at that frontend might send

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is not None:
            if len(v) < 1:
                raise ValueError('Title must be at least 1 character long')
            if len(v) > 200:
                raise ValueError('Title must be no more than 200 characters')
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be no more than 1000 characters')
        return v

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError('Category must be no more than 100 characters')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return v

        # Flexible Boolean: Convert string values like 'true', 'false', '0', '1' to actual booleans
        if isinstance(v, str):
            v_lower = v.lower()
            if v_lower in ['true', '1', 'yes', 'on']:
                return True
            elif v_lower in ['false', '0', 'no', 'off', '']:
                return False
            else:
                # If it's not a recognized string, try to parse as boolean
                raise ValueError(f'Status must be a boolean value, got: {v}')
        elif isinstance(v, int):
            # Convert integers 0 and 1 to booleans
            return bool(v)

        # If it's already a boolean, return as is
        return v

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v is not None:
            # Handle string to integer mapping for compatibility
            if isinstance(v, str):
                priority_map = {
                    'High': 3, 'high': 3, 'HIGH': 3,
                    'Medium': 2, 'medium': 2, 'MEDIUM': 2,
                    'Low': 1, 'low': 1, 'LOW': 1,
                    '3': 3, '2': 2, '1': 1
                }
                if v in priority_map:
                    return priority_map[v]
                try:
                    return int(v)
                except ValueError:
                    raise ValueError('Priority must be "High", "Medium", "Low" or 1, 2, 3')
            elif isinstance(v, int):
                if v not in [1, 2, 3]:
                    raise ValueError('Priority must be 1 (Low), 2 (Medium), or 3 (High)')
                return v
            else:
                try:
                    return int(v)
                except (ValueError, TypeError):
                    raise ValueError('Priority must be "High", "Medium", "Low" or 1, 2, 3')
        return v

class TaskResponse(BaseModel):
    """
    Schema for task response.
    """
    id: int
    title: str
    description: Optional[str] = None
    status: bool
    category: Optional[str] = None
    priority: int
    created_at: datetime
    updated_at: datetime
    user_id: str

class TaskListResponse(BaseModel):
    """
    Schema for task list response.
    """
    tasks: list[TaskResponse]

class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    detail: str