from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
import logging
from services.task_service import create_task, get_tasks_by_user, update_task, delete_task, get_task_by_id, get_dashboard_stats_for_user
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from database.session import get_db_session
from schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse, TaskListResponse
from exceptions.handlers import ValidationError
from config import settings
from middleware.auth import get_current_user

# Create logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_request: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new task for the authenticated user.
    """
    try:
        # Log the current_user object for debugging
        logger.info(f"Authenticated user object: {current_user}")
        print(f"DEBUG AUTH: create_task_endpoint - current_user: {current_user}")
        print(f"DEBUG AUTH: create_task_endpoint - current_user type: {type(current_user)}")

        # Extract user ID from the authenticated user (Better Auth returns dict)
        user_id = current_user.get("id")
        logger.info(f"Extracted user_id from authenticated user: {user_id}")
        print(f"DEBUG AUTH: create_task_endpoint - extracted user_id: {user_id}")

        if not user_id:
            logger.error("User ID not found in authentication token")
            print(f"DEBUG AUTH: create_task_endpoint - ERROR: User ID not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token"
            )

        # Log the task creation attempt
        logger.info(f"Task creation attempt for user ID: {user_id}")

        # Validate the request data
        validated_request = TaskCreate.model_validate(task_request.model_dump())
        logger.debug(f"Validated task request: {validated_request}")

        # Additional validation - check if the user is trying to create too many tasks
        # Get current task count for the user
        from sqlmodel import select
        from models.task import Task
        result = await db.exec(
            select(Task).where(Task.user_id == user_id)
        )
        user_tasks = result.all()

        # Optional: Implement a limit on number of tasks a user can create
        # For now, just log the number of existing tasks
        logger.info(f"User {user_id} currently has {len(user_tasks)} tasks")

        # Create the task
        task = await create_task(
            db_session=db,
            task_in=validated_request,
            user_id=user_id
        )

        # Log successful task creation
        logger.info(f"Task created successfully with ID: {task.id} for user: {user_id}")

        # Optionally broadcast dashboard update (but don't let it fail the main operation)
        try:
            from utils.websocket_manager import broadcast_dashboard_update

            async def broadcast_dashboard_update_task():
                try:
                    dashboard_stats = await get_dashboard_stats_for_user(
                        db_session=db,
                        user_id=user_id  # Use string ID for the service call
                    )
                    await broadcast_dashboard_update(user_id, dashboard_stats)
                except Exception as e:
                    logger.warning(f"Failed to broadcast dashboard update: {str(e)}")

            # Schedule the broadcast without blocking the main operation
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(broadcast_dashboard_update_task())
            except RuntimeError:
                # If no running loop, run in a new thread (fallback)
                import threading
                def run_broadcast():
                    import asyncio
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        new_loop.run_until_complete(broadcast_dashboard_update_task())
                    finally:
                        new_loop.close()

                thread = threading.Thread(target=run_broadcast, daemon=True)
                thread.start()
        except Exception as e:
            logger.warning(f"Failed to initiate dashboard broadcast: {str(e)}")

        # Return the created task
        logger.info(f"Returning created task with ID: {task.id}")
        return TaskResponse.model_validate(task.model_dump())
    except ValueError as e:
        logger.warning(f"Task creation failed due to validation error for user {user_id}: {str(e)}")
        raise ValidationError(str(e))
    except HTTPException as he:
        logger.error(f"HTTP Exception during task creation for user {user_id}: {he.status_code} - {he.detail}")
        # Re-raise HTTP exceptions (like 403)
        raise
    except Exception as e:
        logger.error(f"Unexpected error during task creation for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )

@router.get("/", response_model=TaskListResponse)
async def get_tasks_endpoint(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all tasks for the authenticated user.
    """
    try:
        # Extract user ID from the authenticated user (Better Auth returns dict)
        user_id = current_user.get("id")

        if not user_id:
            logger.error("User ID not found in authentication token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token"
            )

        # Log the task retrieval attempt
        logger.info(f"Task retrieval attempt for user ID: {user_id}")

        # Get tasks for the user
        tasks = await get_tasks_by_user(
            db_session=db,
            user_id=user_id,
            skip=skip,
            limit=limit
        )

        # Convert to response format
        task_responses = [TaskResponse.model_validate(task.model_dump()) for task in tasks]

        # Log successful retrieval
        logger.info(f"Retrieved {len(tasks)} tasks for user: {user_id}")

        # Return the list of tasks
        return TaskListResponse(tasks=task_responses)
    except HTTPException as he:
        logger.error(f"HTTP Exception during task retrieval for user: {he.status_code} - {he.detail}")
        # Re-raise HTTP exceptions (like 403)
        raise
    except Exception as e:
        logger.error(f"Unexpected error during task retrieval: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    try:
        # Extract user ID from the authenticated user (Better Auth returns dict)
        user_id = current_user.get("id")

        if not user_id:
            logger.error(f"User ID not found in authentication token when accessing task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token"
            )

        # Log the task access attempt
        logger.info(f"Task access attempt for task ID: {task_id}, user ID: {user_id}")

        # Get the task
        task = await get_task_by_id(
            db_session=db,
            task_id=task_id,
            user_id=user_id
        )

        # Log successful task access
        logger.info(f"Task {task_id} accessed successfully by user: {user_id}")

        # Return the task
        return TaskResponse.model_validate(task.model_dump())
    except HTTPException as he:
        logger.error(f"HTTP Exception during task access for task {task_id}, user {user_id}: {he.status_code} - {he.detail}")
        # Re-raise HTTP exceptions (like 404, 403)
        raise
    except Exception as e:
        logger.error(f"Unexpected error during task access for task {task_id}, user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}"
        )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_update: TaskUpdateRequest,
    task_id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update a specific task by ID for the authenticated user.
    """
    try:
        # Extract user ID from the authenticated user (Better Auth returns dict)
        user_id = current_user.get("id")

        if not user_id:
            logger.error(f"User ID not found in authentication token when updating task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token"
            )

        # Log the task update attempt
        logger.info(f"Task update attempt for task ID: {task_id}, user ID: {user_id}")

        # Validate the update request - priority conversion is handled by field_validator in model
        validated_update = TaskUpdate.model_validate(task_update.model_dump(exclude_unset=True))

        # Update the task
        task = await update_task(
            db_session=db,
            task_id=task_id,
            task_in=validated_update,
            user_id=user_id
        )

        # Log successful task update
        logger.info(f"Task updated successfully with ID: {task.id} for user: {user_id}")

        # Optionally broadcast dashboard update (but don't let it fail the main operation)
        try:
            from utils.websocket_manager import broadcast_dashboard_update

            async def broadcast_dashboard_update_task():
                try:
                    dashboard_stats = await get_dashboard_stats_for_user(
                        db_session=db,
                        user_id=user_id  # Use string ID for the service call
                    )
                    await broadcast_dashboard_update(user_id, dashboard_stats)
                except Exception as e:
                    logger.warning(f"Failed to broadcast dashboard update: {str(e)}")

            # Schedule the broadcast without blocking the main operation
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(broadcast_dashboard_update_task())
            except RuntimeError:
                # If no running loop, run in a new thread (fallback)
                import threading
                def run_broadcast():
                    import asyncio
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        new_loop.run_until_complete(broadcast_dashboard_update_task())
                    finally:
                        new_loop.close()

                thread = threading.Thread(target=run_broadcast, daemon=True)
                thread.start()
        except Exception as e:
            logger.warning(f"Failed to initiate dashboard broadcast: {str(e)}")

        # Return the updated task
        return TaskResponse.model_validate(task.model_dump())
    except HTTPException as he:
        logger.error(f"HTTP Exception during task update for task {task_id}, user {user_id}: {he.status_code} - {he.detail}")
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f'Update Error: {e}')
        logger.error(f"Unexpected error during task update for task {task_id}, user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task_endpoint(
    task_id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mark a task as complete.
    Phase II spec compliant endpoint: PATCH /api/tasks/{id}/complete
    """
    try:
        # Extract user ID from authenticated user (Better Auth returns dict)
        user_id = current_user.get("id")
        if not user_id:
            logger.error(f"User ID not found in authentication token when completing task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token"
            )

        # Log the task completion attempt
        logger.info(f"Task completion attempt for task ID: {task_id}, user ID: {user_id}")

        # Create update request to mark task as complete
        task_update = TaskUpdateRequest(status=True)
        validated_update = TaskUpdate.model_validate(task_update.model_dump(exclude_unset=True))

        # Update the task (service layer handles ownership verification)
        task = await update_task(
            db_session=db,
            task_id=task_id,
            task_in=validated_update,
            user_id=user_id
        )

        # Log successful completion
        logger.info(f"Task {task_id} marked as complete for user {user_id}")

        # Return the updated task
        return TaskResponse.model_validate(task.model_dump())

    except HTTPException as he:
        logger.error(f"HTTP Exception during task completion for task {task_id}, user {user_id}: {he.status_code} - {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Error completing task {task_id} for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error completing task: {str(e)}"
        )


@router.delete("/{task_id}")
async def delete_task_endpoint(
    task_id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific task by ID for the authenticated user.
    """
    try:
        # Extract user ID from the authenticated user (Better Auth returns dict)
        user_id = current_user.get("id")

        if not user_id:
            logger.error(f"User ID not found in authentication token when deleting task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token"
            )

        # Diagnostic logging
        print(f"\n🗑️ DELETE REQUEST:")
        print(f"  Task ID: {task_id} (type: {type(task_id)})")
        print(f"  User ID: {user_id}")

        # Log the task deletion attempt
        logger.info(f"Task deletion attempt for task ID: {task_id}, user ID: {user_id}")

        # Delete the task
        success = await delete_task(
            db_session=db,
            task_id=task_id,
            user_id=user_id
        )

        if not success:
            print(f"❌ DELETE FAILED - Task {task_id} not found for user {user_id}")
            logger.warning(f"Task deletion failed - task {task_id} not found for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Log successful task deletion
        print(f"✅ DELETE SUCCESS - Task {task_id} deleted")
        logger.info(f"Task deleted successfully with ID: {task_id} for user: {user_id}")

        # Return success message
        return {"message": "Task deleted successfully"}
    except HTTPException as he:
        logger.error(f"HTTP Exception during task deletion for task {task_id}, user {user_id}: {he.status_code} - {he.detail}")
        # Log failures
        logger.warning(f"Task deletion failed for task {task_id}, user {user_id}: {str(he.detail)}")
        # Re-raise HTTP exceptions (like 404, 403)
        raise
    except Exception as e:
        logger.error(f"Unexpected error during task deletion for task {task_id}, user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )