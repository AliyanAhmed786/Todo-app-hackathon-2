from fastapi import Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from models.user import User
from database.session import get_db_session
from config import settings
from middleware.better_auth import get_current_user_from_session

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Dependency to get the current authenticated user from Better Auth session cookie.
    """
    # Get user from Better Auth session validation
    user = await get_current_user_from_session(request)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the resource.
    """
    return user_id == resource_user_id