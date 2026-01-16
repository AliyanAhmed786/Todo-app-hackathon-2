from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel.ext.asyncio.session import AsyncSession
import logging
from services.task_service import (
    get_dashboard_stats_for_user
)
from database.session import get_db_session
from dependencies.auth import get_current_user

# Create logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get dashboard statistics for the user.
    Returns total tasks, completed tasks, and pending tasks counts.
    """
    try:
        # Extract user ID from the authenticated user (now a dict)
        user_id = current_user.get("id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token"
            )

        # Log to see if the hang happens during Auth or during the Data Fetch
        print('---> AUTH SUCCESSFUL')

        # Get dashboard statistics for the user
        stats = await get_dashboard_stats_for_user(
            db_session=db,
            user_id=user_id
        )

        # Log dashboard access for analytics
        logger.info(f"Dashboard stats requested for user {user_id}")

        # Return dashboard statistics
        return stats
    except HTTPException:
        # Re-raise HTTP exceptions (like 403)
        raise
    except Exception as e:
        # Log error for debugging
        logger.error(f"Error retrieving dashboard statistics for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving dashboard statistics: {str(e)}"
        )