"""
Login service for Better Auth database session validation.
This service handles user login using the Better Auth database validation approach.
"""

from sqlmodel.ext.asyncio.session import AsyncSession
from models.user import User
from models.session import Session, SessionCreate
from services.user_service import authenticate_user
from typing import Optional, Tuple
import secrets
from datetime import datetime, timedelta
import logging

# Create logger
logger = logging.getLogger(__name__)


async def login_user(*, db_session: AsyncSession, email: str, password: str) -> Tuple[Optional[User], Optional[Session]]:
    """
    Login a user with Better Auth database session validation approach.

    Args:
        db_session: The database session to use for the operation
        email: The user's email address
        password: The user's password

    Returns:
        Tuple[User, Session]: The authenticated user and session objects, or (None, None) if authentication failed
    """
    # Bcrypt has a 72-byte limit. We check this before anything else.
    if len(password.encode('utf-8')) > 72:
        logger.warning(f"Login failed: Password exceeds 72 bytes for {email}")
        return None, None

    # Authenticate the user
    user = await authenticate_user(
        db_session=db_session,
        email=email,
        password=password
    )

    if not user:
        logger.warning(f"Login failed for email: {email} - invalid credentials")
        return None, None

    # Create a session in the database for Better Auth database validation
    session_expires = datetime.utcnow() + timedelta(minutes=30)  # Default 30-minute session

    # Generate a random session token
    session_token = secrets.token_urlsafe(32)

    # Create session record
    session_data = SessionCreate(
        id=secrets.token_hex(16),  # Generate a unique session ID
        token=session_token,
        user_id=user.id,
        expires_at=session_expires
    )

    # Create session in database
    session = Session(**session_data.model_dump())
    db_session.add(session)
    await db_session.commit()
    await db_session.refresh(session)

    logger.info(f"User logged in successfully: {user.id} ({user.email})")
    return user, session


async def logout_user(*, db_session: AsyncSession, session_token: str) -> bool:
    """
    Logout a user by removing their session from the database.

    Args:
        db_session: The database session to use for the operation
        session_token: The session token to invalidate

    Returns:
        bool: True if the session was successfully removed, False otherwise
    """
    from sqlmodel import select

    # Find the session in the database
    result = await db_session.exec(
        select(Session).where(Session.token == session_token)
    )
    session = result.first()

    if not session:
        logger.warning(f"Attempted to logout with invalid session token")
        return False

    # Delete the session from the database
    await db_session.delete(session)
    await db_session.commit()

    logger.info(f"User logged out successfully: {session.user_id}")
    return True


async def validate_session(*, db_session: AsyncSession, session_token: str) -> Optional[User]:
    """
    Validate a session token against the database.

    Args:
        db_session: The database session to use for the operation
        session_token: The session token to validate

    Returns:
        User: The user associated with the session if valid, None otherwise
    """
    from sqlmodel import select

    # Find the session in the database
    result = await db_session.exec(
        select(Session)
        .where(Session.token == session_token)
        .where(Session.expires_at > datetime.utcnow())
    )
    session = result.first()

    if not session:
        logger.warning(f"Invalid or expired session token used")
        return None

    # Get the associated user
    from services.user_service import get_user_by_id
    user = await get_user_by_id(db_session=db_session, user_id=session.user_id)

    if not user:
        logger.warning(f"Session exists for non-existent user: {session.user_id}")
        # Clean up the orphaned session
        await db_session.delete(session)
        await db_session.commit()
        return None

    logger.info(f"Session validated successfully for user: {user.id}")
    return user