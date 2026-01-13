"""
Logout service for Better Auth database session validation.
This service handles user logout operations using the Better Auth database validation approach.
"""

from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, Any
import logging

# Create logger
logger = logging.getLogger(__name__)


async def logout_user(*, db_session: AsyncSession, session_token: str) -> Dict[str, Any]:
    """
    Logout a user by removing their session from the database.

    Args:
        db_session: The database session to use for the operation
        session_token: The session token to invalidate

    Returns:
        Dict[str, Any]: Result containing success status and any relevant data
    """
    try:
        # Use the session service to delete the session
        from services.session_service import delete_session
        success = await delete_session(
            db_session=db_session,
            session_token=session_token
        )

        if success:
            logger.info(f"User successfully logged out for session token: {session_token[:20]}...")
            return {
                "success": True,
                "message": "Successfully logged out"
            }
        else:
            logger.warning(f"Logout attempted for non-existent or already deleted session: {session_token[:20]}...")
            return {
                "success": True,  # Still consider it successful since the goal is to end the session
                "message": "Session already ended or invalid"
            }

    except Exception as e:
        logger.error(f"Error during logout process: {str(e)}")
        return {
            "success": False,
            "message": f"Error during logout: {str(e)}"
        }


async def logout_user_by_id(*, db_session: AsyncSession, user_id: str) -> Dict[str, Any]:
    """
    Logout a user by removing all their sessions from the database.

    Args:
        db_session: The database session to use for the operation
        user_id: The ID of the user to log out

    Returns:
        Dict[str, Any]: Result containing success status and any relevant data
    """
    try:
        # Use the session service to delete all sessions for the user
        from services.session_service import delete_user_sessions
        success = await delete_user_sessions(
            db_session=db_session,
            user_id=user_id
        )

        if success:
            logger.info(f"All sessions successfully cleared for user: {user_id}")
            return {
                "success": True,
                "message": "Successfully logged out from all devices"
            }
        else:
            logger.warning(f"Failed to clear sessions for user: {user_id}")
            return {
                "success": False,
                "message": "Failed to clear user sessions"
            }

    except Exception as e:
        logger.error(f"Error during user logout by ID: {str(e)}")
        return {
            "success": False,
            "message": f"Error during logout: {str(e)}"
        }