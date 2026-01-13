"""
Session management service for Better Auth database session validation.
This service handles session creation, validation, and cleanup operations.
"""

from sqlmodel.ext.asyncio.session import AsyncSession
from models.session import Session
from models.user import User
from typing import Optional
import secrets
from datetime import datetime, timedelta
import logging

# Create logger
logger = logging.getLogger(__name__)


async def create_session(*, db_session: AsyncSession, user_id: str, expires_in_minutes: int = 30) -> Optional[Session]:
    """
    Create a new session in the database for Better Auth database validation.

    Args:
        db_session: The database session to use for the operation
        user_id: The ID of the user to create a session for
        expires_in_minutes: Number of minutes until the session expires (default 30)

    Returns:
        Session: The created session object, or None if creation failed
    """
    try:
        # Create session expiration time
        session_expires = datetime.utcnow() + timedelta(minutes=expires_in_minutes)

        # Generate a random session token
        session_token = secrets.token_urlsafe(32)

        # Create session record
        from models.session import SessionCreate
        session_data = SessionCreate(
            id=secrets.token_hex(16),  # Generate a unique session ID
            token=session_token,
            user_id=user_id,
            expires_at=session_expires
        )

        # Create session in database
        session = Session(**session_data.model_dump())
        db_session.add(session)
        await db_session.commit()
        await db_session.refresh(session)

        logger.info(f"Session created successfully for user: {user_id}")
        return session
    except Exception as e:
        logger.error(f"Error creating session for user {user_id}: {str(e)}")
        return None


async def validate_session(*, db_session: AsyncSession, session_token: str) -> Optional[User]:
    """
    Validate a session token against the database.
    Optimized to use a single JOIN query instead of two separate queries.

    Args:
        db_session: The database session to use for the operation
        session_token: The session token to validate

    Returns:
        User: The user associated with the session if valid, None otherwise
    """
    from sqlmodel import select

    try:
        # OPTIMIZED: Find the session AND user in a single JOIN query
        # This reduces database round-trips from 2 to 1
        result = await db_session.exec(
            select(Session, User)
            .join(User, Session.user_id == User.id)
            .where(Session.token == session_token)
            .where(Session.expires_at > datetime.utcnow())
        )
        session_user_tuple = result.first()

        if not session_user_tuple:
            logger.warning(f"Invalid or expired session token used")
            return None

        session, user = session_user_tuple

        if not user:
            logger.warning(f"Session exists for non-existent user: {session.user_id}")
            # Clean up the orphaned session
            await db_session.delete(session)
            await db_session.commit()
            return None

        logger.info(f"Session validated successfully for user: {user.id}")
        return user
    except Exception as e:
        logger.error(f"Error validating session: {str(e)}")
        return None


async def delete_session(*, db_session: AsyncSession, session_token: str) -> bool:
    """
    Delete a session from the database.

    Args:
        db_session: The database session to use for the operation
        session_token: The session token to delete

    Returns:
        bool: True if the session was successfully removed, False otherwise
    """
    from sqlmodel import select

    try:
        # Find the session in the database
        result = await db_session.exec(
            select(Session).where(Session.token == session_token)
        )
        session = result.first()

        if not session:
            logger.warning(f"Attempted to delete non-existent session token")
            return False

        # Delete the session from the database
        await db_session.delete(session)
        await db_session.commit()

        logger.info(f"Session deleted successfully: {session.user_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        return False


async def delete_user_sessions(*, db_session: AsyncSession, user_id: str) -> bool:
    """
    Delete all sessions for a specific user (useful when user is deleted).

    Args:
        db_session: The database session to use for the operation
        user_id: The ID of the user whose sessions should be deleted

    Returns:
        bool: True if sessions were successfully removed, False otherwise
    """
    from sqlmodel import select

    try:
        # Find all sessions for the user
        result = await db_session.exec(
            select(Session).where(Session.user_id == user_id)
        )
        sessions = result.all()

        # Delete each session
        for session in sessions:
            await db_session.delete(session)

        await db_session.commit()

        logger.info(f"Deleted {len(sessions)} sessions for user: {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting user sessions: {str(e)}")
        return False


async def refresh_session(*, db_session: AsyncSession, session_token: str, expires_in_minutes: int = 30) -> Optional[Session]:
    """
    Refresh an existing session by creating a new one and deleting the old one.

    Args:
        db_session: The database session to use for the operation
        session_token: The current session token to refresh
        expires_in_minutes: Number of minutes until the new session expires (default 30)

    Returns:
        Session: The new session object, or None if refresh failed
    """
    from sqlmodel import select

    try:
        # Find the current session
        result = await db_session.exec(
            select(Session).where(Session.token == session_token)
        )
        current_session = result.first()

        if not current_session:
            logger.warning(f"Attempted to refresh non-existent session token")
            return None

        user_id = current_session.user_id

        # Delete the old session
        await db_session.delete(current_session)

        # Create a new session
        new_session = await create_session(
            db_session=db_session,
            user_id=user_id,
            expires_in_minutes=expires_in_minutes
        )

        if new_session:
            logger.info(f"Session refreshed successfully for user: {user_id}")
            return new_session
        else:
            logger.error(f"Failed to create new session during refresh for user: {user_id}")
            return None
    except Exception as e:
        logger.error(f"Error refreshing session: {str(e)}")
        return None