import re
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import field_validator, model_validator

class PriorityEnum(int, Enum):
    """
    Enum for task priority levels.
    """
    LOW = 1
    MEDIUM = 2
    HIGH = 3

def sanitize_input(text: str) -> str:
    """
    Sanitize input by removing potentially dangerous characters and patterns.
    """
    if not text:
        return text

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)

    # Remove script tags and other potentially dangerous HTML
    sanitized = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

    # Remove potential SQL injection patterns
    sanitized = re.sub(r"(?i)(union\s+select|drop\s+\w+|create\s+\w+|delete\s+from|insert\s+into|update\s+\w+\s+set)", '', sanitized)

    return sanitized.strip()

class TaskBase(SQLModel):
    """
    Base class for Task model with common fields.
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: bool = Field(default=False)
    category: Optional[str] = Field(default=None, max_length=100)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)

    @field_validator('title')
    @classmethod
    def validate_and_sanitize_title(cls, v):
        if not v:
            return v
        # Sanitize the title
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 1 or len(sanitized) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return sanitized

    @field_validator('description')
    @classmethod
    def validate_and_sanitize_description(cls, v):
        if not v:
            return v
        # Sanitize the description
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) > 1000:
            raise ValueError('Description must be no more than 1000 characters')
        return sanitized

    @field_validator('category')
    @classmethod
    def validate_and_sanitize_category(cls, v):
        if not v:
            return v
        # Sanitize the category
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) > 100:
            raise ValueError('Category must be no more than 100 characters')
        return sanitized

class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to User with CASCADE DELETE for Better Auth integration
    user_id: str = Field(foreign_key="user.id", ondelete="CASCADE")

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks", sa_relationship_kwargs={"lazy": "selectin"})

    def __str__(self):
        return f"Task(id={self.id}, title={self.title}, status={self.status})"

class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: str

class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: Optional[str] = Field(default=None, max_length=100)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)

class TaskUpdate(SQLModel):
    """
    Schema for updating task information.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[bool] = None
    category: Optional[str] = Field(default=None, max_length=100)
    priority: Optional[int] = None  # Updated to use int with validator

    @field_validator('priority', mode='before')
    @classmethod
    def validate_priority(cls, v):
        if v is None:
            return v

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

class TaskPublic(TaskBase):
    """
    Public schema for task (without user details).
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: str