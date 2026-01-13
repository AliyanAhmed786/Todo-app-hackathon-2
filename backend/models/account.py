"""
Better Auth Account model for database session validation.
This model represents the account table that Better Auth would use
for managing user accounts and providers.
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


class AccountBase(SQLModel):
    """
    Base class for Account model with common fields.
    """
    user_id: str = Field(max_length=100)  # Reference to Better Auth user ID
    provider_id: str = Field(max_length=100)  # Provider identifier (e.g., "email", "google")
    provider_account_id: str = Field(max_length=200)  # Account identifier from provider

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

    @field_validator('provider_id')
    @classmethod
    def validate_and_sanitize_provider_id(cls, v):
        if not v:
            return v
        # Sanitize the provider_id
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 1 or len(sanitized) > 100:
            raise ValueError('Provider ID must be between 1 and 100 characters')
        return sanitized.strip()

    @field_validator('provider_account_id')
    @classmethod
    def validate_and_sanitize_provider_account_id(cls, v):
        if not v:
            return v
        # Sanitize the provider_account_id
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 1 or len(sanitized) > 200:
            raise ValueError('Provider account ID must be between 1 and 200 characters')
        return sanitized.strip()


class Account(AccountBase, table=True):
    """
    Account model representing Better Auth account data for managing user accounts and providers.
    """
    id: Optional[str] = Field(default=None, primary_key=True, max_length=100)
    user_id: str = Field(max_length=100)  # Reference to Better Auth user ID
    provider_id: str = Field(max_length=100)  # Provider identifier (e.g., "email", "google")
    provider_account_id: str = Field(max_length=200)  # Account identifier from provider
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user (if needed)
    # user: Optional["User"] = Relationship(back_populates="accounts", sa_relationship_args=[dict(lazy="selectin")])

    def __str__(self):
        return f"Account(id={self.id}, user_id={self.user_id}, provider_id={self.provider_id})"


class AccountRead(AccountBase):
    """
    Schema for reading account data.
    """
    id: str
    created_at: datetime
    updated_at: datetime


class AccountCreate(AccountBase):
    """
    Schema for creating a new account.
    """
    id: Optional[str] = None
    user_id: str
    provider_id: str
    provider_account_id: str


class AccountUpdate(SQLModel):
    """
    Schema for updating account information.
    """
    user_id: Optional[str] = None
    provider_id: Optional[str] = None
    provider_account_id: Optional[str] = None


class AccountPublic(AccountBase):
    """
    Public schema for account.
    """
    id: str