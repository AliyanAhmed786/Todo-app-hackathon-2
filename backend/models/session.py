"""
Better Auth Session model for database session validation.
This model represents the session table that Better Auth would use
for database session validation strategy.
"""

import re
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from pydantic import field_validator


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


class SessionBase(SQLModel):
    """
    Base class for Session model with common fields.
    """
    token: str = Field(unique=True, max_length=500)
    user_id: str = Field(max_length=100, foreign_key="user.id", ondelete="CASCADE")  # Better Auth user ID
    expires_at: datetime = Field(sa_column_kwargs={"nullable": False})

    @field_validator('token')
    @classmethod
    def validate_and_sanitize_token(cls, v):
        if not v:
            return v
        # Sanitize the token
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 10 or len(sanitized) > 500:
            raise ValueError('Session token must be between 10 and 500 characters')
        return sanitized.strip()

    @field_validator('user_id')
    @classmethod
    def validate_and_sanitize_user_id(cls, v):
        if not v:
            return v
        # Sanitize the user_id
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 1 or len(sanitized) > 100:
            raise ValueError('User ID must be between 1 and 100 characters')
        return sanitized.strip()


class Session(SessionBase, table=True):
    """
    Session model representing Better Auth session data for database validation.
    """
    id: Optional[str] = Field(default=None, primary_key=True, max_length=100)
    token: str = Field(unique=True, max_length=500)
    user_id: str = Field(max_length=100, foreign_key="user.id", ondelete="CASCADE")  # Better Auth user ID
    expires_at: datetime = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user (if needed)
    # user: Optional["User"] = Relationship(back_populates="sessions")

    def __str__(self):
        return f"Session(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})"


class SessionRead(SessionBase):
    """
    Schema for reading session data (without sensitive information).
    """
    id: str
    created_at: datetime
    updated_at: datetime


class SessionCreate(SessionBase):
    """
    Schema for creating a new session.
    """
    id: Optional[str] = None
    token: str
    user_id: str
    expires_at: datetime


class SessionUpdate(SQLModel):
    """
    Schema for updating session information.
    """
    token: Optional[str] = None
    user_id: Optional[str] = None
    expires_at: Optional[datetime] = None


class SessionPublic(SessionBase):
    """
    Public schema for session (without sensitive information).
    """
    id: str