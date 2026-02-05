"""
Chat-specific authentication dependencies for chatbot backend.
"""

from fastapi import Depends, HTTPException, status
from typing import Optional, Union, Dict, Any
from sqlmodel import Session
from models.user import User
from dependencies.auth import get_current_user


async def get_current_chat_user(
    user_id: str,
    current_user: Union[User, Dict[str, Any]] = Depends(get_current_user)
) -> Union[User, Dict[str, Any]]:
    """
    Get the current authenticated user for chat operations.

    Args:
        user_id: The user ID from the path parameter
        current_user: The authenticated user from JWT token (could be User object or dict)

    Returns:
        User or Dict: The authenticated user object/dict

    Raises:
        HTTPException: If user is not authenticated or user_id doesn't match token
    """
    try:
        # Use dictionary-safe access for current_user
        # Handle both User object and dictionary cases
        if isinstance(current_user, dict):
            current_user_id = str(current_user.get('id', ''))
        else:
            current_user_id = str(getattr(current_user, 'id', ''))

        # Ensure both sides of comparison are strings
        if str(current_user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: user_id mismatch"
            )

        return current_user

    except Exception as e:
        # Error Response Stability: Use required format
        print(f'❌ BACKEND CRASH: {e}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


def verify_user_access(
    user_id: str,
    requesting_user: Union[User, Dict[str, Any]] = Depends(get_current_chat_user)
) -> bool:
    """
    Verify that the requesting user has access to the specified user resources.

    Args:
        user_id: The user ID to check access for
        requesting_user: The user making the request (could be User object or dict)

    Returns:
        bool: True if access is granted
    """
    try:
        # Use dictionary-safe access
        if isinstance(requesting_user, dict):
            requesting_user_id = str(requesting_user.get('id', ''))
        else:
            requesting_user_id = str(getattr(requesting_user, 'id', ''))

        # Ensure both sides of comparison are strings
        return str(requesting_user_id) == str(user_id)

    except Exception as e:
        # Error Response Stability: Use required format
        print(f'❌ BACKEND CRASH: {e}')
        return False


def validate_conversation_access(
    conversation_id: str,
    user: Union[User, Dict[str, Any]] = Depends(get_current_chat_user)
) -> bool:
    """
    Validate that the user has access to the specified conversation.

    Args:
        conversation_id: The conversation ID to validate access for
        user: The user requesting access (could be User object or dict)

    Returns:
        bool: True if access is granted
    """
    try:
        # Use dictionary-safe access
        if isinstance(user, dict):
            user_id = str(user.get('id', ''))
        else:
            user_id = str(getattr(user, 'id', ''))

        # This would typically query the database to check if the conversation
        # belongs to the user, but we return True for now as a placeholder
        # until the database session and query logic is implemented
        return True

    except Exception as e:
        # Error Response Stability: Use required format
        print(f'❌ BACKEND CRASH: {e}')
        return False