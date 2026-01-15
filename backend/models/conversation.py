"""
Conversation model for chatbot backend.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
from uuid import uuid4
import json

if TYPE_CHECKING:
    from models.user import User
    from models.message import Message


class ConversationBase(SQLModel):
    """Base class for Conversation model."""
    pass


class Conversation(ConversationBase, table=True):
    """Conversation entity representing a chat session."""

    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, max_length=100)
    user_id: str = Field(foreign_key="user.id", nullable=False, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    meta_data: Optional[str] = Field(default=None, sa_column_kwargs={"name": "metadata"})

    # Relationship to User
    user: "User" = Relationship(back_populates="conversations")

    # Relationship to Messages
    messages: list["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    user_id: str
    meta_data: Optional[str] = None


class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    meta_data: Optional[str] = None
    message_count: Optional[int] = None


class ConversationUpdate(SQLModel):
    """Schema for updating conversation data."""
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    meta_data: Optional[str] = None