"""
Message model for chatbot backend.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
from uuid import uuid4

if TYPE_CHECKING:
    from models.conversation import Conversation


class MessageBase(SQLModel):
    """Base class for Message model."""
    pass


class Message(MessageBase, table=True):
    """Message entity representing a chat message."""

    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, max_length=100)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False, max_length=100)
    sender: str = Field(sa_column_kwargs={
        "nullable": False,
        "server_default": "user",
        "comment": "Either 'user' or 'agent'"
    })
    content: str = Field(sa_column_kwargs={"nullable": False})
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    meta_data: Optional[str] = Field(default=None, sa_column_kwargs={"name": "meta_data"})

    # Relationship to Conversation
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    conversation_id: str
    sender: str  # Either 'user' or 'agent'
    content: str
    meta_data: Optional[str] = None


class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: str
    conversation_id: str
    sender: str
    content: str
    timestamp: datetime
    meta_data: Optional[str] = None


class MessageUpdate(SQLModel):
    """Schema for updating message data."""
    content: Optional[str] = None
    meta_data: Optional[str] = None