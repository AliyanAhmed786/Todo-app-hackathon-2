"""
Authentication schemas for Better Auth database session validation.
This module contains request and response validation schemas for authentication endpoints.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class UserCreateRequest(BaseModel):
    """
    Schema for user creation requests in Better Auth database validation approach.
    """
    name: str
    email: EmailStr
    password: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name is required')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if len(v.strip()) > 100:
            raise ValueError('Name must be no more than 100 characters')

        # Additional validation to ensure name only contains valid characters
        if not re.match(r'^[a-zA-Z0-9\s\'\-]+$', v.strip()):
            raise ValueError('Name contains invalid characters')

        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email is required')
        if len(v) > 200:
            raise ValueError('Email must be no more than 200 characters')
        return v.lower().strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password must be no more than 128 characters')

        # Check for at least one uppercase, lowercase, digit, and special character
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one digit')

        return v


class UserLoginRequest(BaseModel):
    """
    Schema for user login requests in Better Auth database validation approach.
    """
    email: EmailStr
    password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email is required')
        if len(v) > 200:
            raise ValueError('Email must be no more than 200 characters')
        return v.lower().strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        if len(v) < 1:
            raise ValueError('Password cannot be empty')
        if len(v) > 128:
            raise ValueError('Password must be no more than 128 characters')
        return v


class AuthResponse(BaseModel):
    """
    Schema for authentication responses in Better Auth database validation approach.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SessionResponse(BaseModel):
    """
    Schema for session validation responses in Better Auth database validation approach.
    """
    user: Optional[dict] = None
    token: Optional[str] = None


class BetterAuthRegistrationRequest(BaseModel):
    """
    Schema for Better Auth registration requests with enhanced validation.
    """
    name: str
    email: EmailStr
    password: str
    # Optional fields for future expansion
    image: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_better_auth_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name is required')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if len(v.strip()) > 100:
            raise ValueError('Name must be no more than 100 characters')

        # Additional validation to ensure name only contains valid characters
        if not re.match(r'^[a-zA-Z0-9\s\'\-]+$', v.strip()):
            raise ValueError('Name contains invalid characters')

        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_better_auth_email(cls, v):
        if not v:
            raise ValueError('Email is required')
        if len(v) > 200:
            raise ValueError('Email must be no more than 200 characters')
        return v.lower().strip()

    @field_validator('password')
    @classmethod
    def validate_better_auth_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password must be no more than 128 characters')

        # Check for at least one uppercase, lowercase, digit
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one digit')

        return v

    @field_validator('image')
    @classmethod
    def validate_image_url(cls, v):
        if v is None:
            return v

        if len(v) > 500:
            raise ValueError('Image URL must be no more than 500 characters')

        # Basic URL validation
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Image URL must be a valid URL starting with http:// or https://')

        return v