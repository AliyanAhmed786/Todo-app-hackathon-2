"""
Backend authentication middleware for Better Auth database session validation.
This middleware validates sessions by querying the Better Auth session table in Neon DB
instead of using JWT token decoding, implementing the shared database strategy.
"""
from fastapi import HTTPException, Request, status
from .better_auth import get_current_user_from_session, verify_user_owns_resource as db_verify_user_owns_resource
import logging

# Create logger
logger = logging.getLogger(__name__)

async def get_current_user(request: Request) -> dict:
    """
    Get the current user from the Better Auth database session.

    Args:
        request: The incoming request object

    Returns:
        dict: The user information from the database session
    """
    # Use the database session validation approach
    return await get_current_user_from_session(request)

def verify_user_owns_resource(authenticated_user: dict, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the requested resource.
    Uses database session validation approach.

    Args:
        authenticated_user: The authenticated user dictionary from database session
        resource_user_id: The user ID associated with the resource

    Returns:
        bool: True if the user owns the resource, False otherwise
    """
    # Extract the user ID from the authenticated user
    user_id = authenticated_user.get("id")

    # Use the database verification function
    return db_verify_user_owns_resource(user_id, resource_user_id)