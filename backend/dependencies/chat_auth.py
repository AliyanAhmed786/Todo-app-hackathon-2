"""
Chat-specific authentication dependencies for chatbot backend.
"""

from fastapi import Depends, HTTPException, status
from typing import Optional
from sqlmodel import Session
from models.user import User
from dependencies.auth import get_current_user
from uuid import UUID


async def get_current_chat_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current authenticated user for chat operations.

    Args:
        user_id: The user ID from the path parameter
        current_user: The authenticated user from JWT token

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If user is not authenticated or user_id doesn't match token
    """
    # Verify that the user_id in the path matches the user in the JWT token
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch"
        )

    return current_user


def verify_user_access(
    user_id: str,
    requesting_user: User = Depends(get_current_chat_user)
) -> bool:
    """
    Verify that the requesting user has access to the specified user resources.

    Args:
        user_id: The user ID to check access for
        requesting_user: The user making the request

    Returns:
        bool: True if access is granted
    """
    if str(requesting_user.id) != user_id:
        return False

    return True


def validate_conversation_access(
    conversation_id: UUID,
    user: User = Depends(get_current_chat_user)
) -> bool:
    """
    Validate that the user has access to the specified conversation.

    Args:
        conversation_id: The conversation ID to validate access for
        user: The user requesting access

    Returns:
        bool: True if access is granted
    """
    # This would typically query the database to check if the conversation
    # belongs to the user, but we return True for now as a placeholder
    # until the database session and query logic is implemented
    return True