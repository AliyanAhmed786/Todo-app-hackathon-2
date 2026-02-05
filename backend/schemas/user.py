from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    """
    Schema for creating a new user.
    """
    name: str
    email: EmailStr
    password: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v) < 1:
            raise ValueError('Name is required')
        if len(v) > 100:
            raise ValueError('Name must be no more than 100 characters')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v.encode('utf-8')) > 72:  # ADD THIS LINE
            raise ValueError('Password cannot exceed 72 bytes')  # ADD THIS LINE
        return v

class UserLoginRequest(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    """
    Schema for authentication responses.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    """
    Schema for user response.
    """
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    detail: str

class TokenPayload(BaseModel):
    """
    Schema for token payload.
    """
    sub: str
    exp: int
    type: str