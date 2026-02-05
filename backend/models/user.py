import re
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
import uuid
from pydantic import field_validator
from pydantic.networks import EmailStr
from models.conversation import Conversation

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

class UserBase(SQLModel):
    """
    Base class for User model with common fields.
    """
    name: str = Field(max_length=100)
    email: EmailStr = Field(unique=True, max_length=200)

    @field_validator('name')
    @classmethod
    def validate_and_sanitize_name(cls, v):
        if not v:
            return v
        # Sanitize the name
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 1 or len(sanitized) > 100:
            raise ValueError('Name must be between 1 and 100 characters')
        # Ensure it only contains valid characters (letters, numbers, spaces, hyphens, apostrophes)
        if not re.match(r'^[a-zA-Z0-9\s\'\-]+$', sanitized):
            raise ValueError('Name contains invalid characters')
        return sanitized.strip()

    @field_validator('email', mode='before')
    @classmethod
    def validate_and_sanitize_email(cls, v):
        if not v:
            return v
        # Sanitize the email
        sanitized = sanitize_input(v)
        # Additional validation - basic email format check
        if len(sanitized) > 200:
            raise ValueError('Email must be no more than 200 characters')
        # The EmailStr field type will handle email format validation automatically
        return sanitized.lower().strip()

class User(UserBase, table=True):
    """
    User model representing an authenticated user.
    Updated to work with Better Auth string-based IDs for database session validation.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=100)
    name: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=200)
    email_verified: bool = Field(default=False)
    password_hash: str = Field(sa_column_kwargs={"nullable": False})
    image: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    # Relationship to conversations
    conversations: List["Conversation"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: str
    email_verified: bool
    image: Optional[str]
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

    @field_validator('password', mode='before')
    @classmethod
    def validate_password_length(cls, v):
        if v is None:
            return v
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes')
        return v

class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    name: Optional[str] = None
    email: Optional[str] = None

class UserLogin(SQLModel):
    """
    Schema for user login.
    """
    email: str
    password: str

    @field_validator('password', mode='before')
    @classmethod
    def validate_password_length(cls, v):
        if v is None:
            return v
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes')
        return v

class UserPublic(UserBase):
    """
    Public schema for user (without sensitive information).
    """
    id: str
    email_verified: bool
    image: Optional[str]