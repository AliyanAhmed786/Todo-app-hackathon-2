"""
Better Auth Verification model for database session validation.
This model represents the verification table that Better Auth would use
for email verification and other verification purposes.
"""

import re
from sqlmodel import SQLModel, Field
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


class VerificationBase(SQLModel):
    """
    Base class for Verification model with common fields.
    """
    identifier: str = Field(max_length=200)  # Identifier for verification (email, phone, etc.)
    value: str = Field(max_length=500)  # Verification value
    expires_at: datetime = Field(sa_column_kwargs={"nullable": False})

    @field_validator('identifier')
    @classmethod
    def validate_and_sanitize_identifier(cls, v):
        if not v:
            return v
        # Sanitize the identifier
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 1 or len(sanitized) > 200:
            raise ValueError('Identifier must be between 1 and 200 characters')
        return sanitized.strip()

    @field_validator('value')
    @classmethod
    def validate_and_sanitize_value(cls, v):
        if not v:
            return v
        # Sanitize the value
        sanitized = sanitize_input(v)
        # Additional validation
        if len(sanitized) < 1 or len(sanitized) > 500:
            raise ValueError('Value must be between 1 and 500 characters')
        return sanitized.strip()


class Verification(VerificationBase, table=True):
    """
    Verification model representing Better Auth verification data for email verification and other purposes.
    """
    id: Optional[str] = Field(default=None, primary_key=True, max_length=100)
    identifier: str = Field(max_length=200)  # Identifier for verification (email, phone, etc.)
    value: str = Field(max_length=500)  # Verification value
    expires_at: datetime = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self):
        return f"Verification(id={self.id}, identifier={self.identifier}, expires_at={self.expires_at})"


class VerificationRead(VerificationBase):
    """
    Schema for reading verification data.
    """
    id: str
    created_at: datetime


class VerificationCreate(VerificationBase):
    """
    Schema for creating a new verification.
    """
    id: Optional[str] = None
    identifier: str
    value: str
    expires_at: datetime


class VerificationUpdate(SQLModel):
    """
    Schema for updating verification information.
    """
    identifier: Optional[str] = None
    value: Optional[str] = None
    expires_at: Optional[datetime] = None


class VerificationPublic(VerificationBase):
    """
    Public schema for verification.
    """
    id: str