"""
Better Auth middleware for database session validation.
This middleware validates sessions by querying the Better Auth session table in Neon DB
instead of using JWT token decoding, implementing the shared database strategy.
"""

from fastapi import HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from database.session import get_db_session
from models.user import User
import logging
from typing import Optional
from services.session_service import validate_session
from database.connection import engine  # Import the engine


# Create logger
logger = logging.getLogger(__name__)


async def validate_session_from_database(request: Request) -> Optional[str]:
    """
    Validate session by querying the Better Auth session table in the database.
    This implements the shared database session validation strategy.

    Args:
        request: The incoming request object

    Returns:
        str: The user ID if session is valid, None otherwise
    """
    # Bearer Token Fallback: Check both cookies and headers
    session_token = request.cookies.get("better-auth.session_token")
    if not session_token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            session_token = auth_header[len('Bearer '):].strip()

    if not session_token:
        logger.warning("No session token found in cookies or headers")
        return None

    # Use the session service to validate the session with context manager
    async with AsyncSession(engine) as db:
        try:
            user = await validate_session(db_session=db, session_token=session_token)

            if not user:
                logger.warning(f"No valid session found for token: {session_token[:20]}...")
                return None

            # Session is valid, return the user ID
            logger.info(f"Session validated successfully for user: {user.id}")
            return user.id

        except Exception as e:
            logger.error(f"Error validating session from database: {str(e)}")
            raise
        # The async with block handles resource cleanup automatically


async def get_current_user_from_session(request: Request) -> dict:
    """
    Get the current user from the Better Auth database session.
    Optimized to use a single database connection.

    Args:
        request: The incoming request object

    Returns:
        dict: The user information from the database session

    Raises:
        HTTPException: If the session is invalid or expired
    """
    # Detailed logging for debugging
    print(f"DEBUG AUTH: Request cookies: {dict(request.cookies)}")
    print(f"DEBUG AUTH: Request headers keys: {list(request.headers.keys())}")

    # Get session token from cookies or headers
    session_token = request.cookies.get("better-auth.session_token")
    print(f"DEBUG AUTH: Session token from cookies (better-auth.session_token): {'Found' if session_token else 'Not found'}")

    # Also check for alternative cookie names that might be used by Better Auth
    if not session_token:
        session_token = request.cookies.get("session_token")
        print(f"DEBUG AUTH: Session token from cookies (session_token): {'Found' if session_token else 'Not found'}")

    if not session_token:
        session_token = request.cookies.get("__Secure-better-auth.session_token")  # Secure version
        print(f"DEBUG AUTH: Session token from cookies (__Secure-better-auth.session_token): {'Found' if session_token else 'Not found'}")

    if not session_token:
        auth_header = request.headers.get('Authorization')
        print(f"DEBUG AUTH: Authorization header: {'Found' if auth_header else 'Not found'}")

        if auth_header and auth_header.startswith('Bearer '):
            session_token = auth_header[len('Bearer '):].strip()
            print(f"DEBUG AUTH: Session token from Authorization header: {'Found' if session_token else 'Not found'}")

    if not session_token:
        logger.warning("No session token found - user not authenticated")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required - no session token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use a SINGLE database session for both validation and user fetch
    async with AsyncSession(engine) as db:
        try:
            logger.info(f"Validating session for token: {session_token[:10]}...")

            # Validate session and get user in ONE database query
            user = await validate_session(db_session=db, session_token=session_token)

            if not user:
                # The token exists but is invalid/expired
                logger.warning("Session token exists but is invalid or expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Session has expired. Please log in again.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Session validation already retrieved the user, no need for second query
            logger.info(f"Session verified successfully for user: {user.id}")

            # Create flat user dict structure
            user_dict = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "email_verified": user.email_verified
            }
            print(f"DEBUG AUTH: Returning user dict: {user_dict}")

            # Return user information in a format compatible with Better Auth
            return user_dict

        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Error in get_current_user_from_session: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error validating session: {str(e)}"
            )
        # The async with block handles resource cleanup automatically


def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the requested resource.

    Args:
        user_id: The ID of the authenticated user
        resource_user_id: The user ID associated with the resource

    Returns:
        bool: True if the user owns the resource, False otherwise
    """
    if user_id != resource_user_id:
        logger.warning(f"User ID mismatch: authenticated={user_id}, resource={resource_user_id}")
        return False

    logger.info(f"Resource ownership verified for user: {user_id}")
    return True