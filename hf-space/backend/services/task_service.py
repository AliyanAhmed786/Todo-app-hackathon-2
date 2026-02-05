from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models.task import Task, TaskCreate, TaskUpdate, TaskRead, PriorityEnum
from models.user import User
from exceptions.handlers import TaskNotFoundError, UnauthorizedAccessError
from datetime import datetime
from typing import List, Optional, Dict

async def create_task(*, db_session: AsyncSession, task_in: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for the given user.
    """
    # Create task object with user_id - priority conversion is now handled by field_validator in model
    task = Task.model_validate(task_in.model_dump(), update={"user_id": user_id})

    # Add to database
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    return task

async def get_task_by_id(*, db_session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a task by its ID, ensuring it belongs to the given user.
    """
    # Get the task
    task = await db_session.get(Task, task_id)

    if task is None:
        raise TaskNotFoundError(task_id)

    # Check if the task belongs to the user
    if task.user_id != user_id:
        raise UnauthorizedAccessError()

    return task

async def get_tasks_by_user(*, db_session: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
    """
    Get all tasks for a specific user.
    """
    # Create query to get tasks for the specific user
    statement = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
    result = await db_session.exec(statement)
    tasks = result.all()

    return tasks

async def update_task(*, db_session: AsyncSession, task_id: int, task_in: TaskUpdate, user_id: str) -> Task:
    """
    Update a task, ensuring it belongs to the given user.
    """
    # Get the existing task
    task = await get_task_by_id(db_session=db_session, task_id=task_id, user_id=user_id)

    # Prepare update data - priority conversion is now handled by field_validator in model
    update_data = task_in.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    # Update the task
    task.sqlmodel_update(update_data)

    # Commit changes
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    return task

async def delete_task(*, db_session: AsyncSession, task_id: int, user_id: str) -> bool:
    """
    Delete a task, ensuring it belongs to the given user.
    Returns True if the task was deleted, False otherwise.
    """
    # Get the task (this will raise an exception if not found or not owned by user)
    task = await get_task_by_id(db_session=db_session, task_id=task_id, user_id=user_id)

    # Delete the task
    await db_session.delete(task)
    await db_session.commit()

    return True

async def get_task_count_for_user(*, db_session: AsyncSession, user_id: str) -> int:
    """
    Get the total count of tasks for a specific user.
    """
    from sqlalchemy import func
    statement = select(func.count(Task.id)).where(Task.user_id == user_id)
    result = await db_session.exec(statement)
    count = result.one() or 0
    return count

async def get_completed_tasks_for_user(*, db_session: AsyncSession, user_id: str) -> List[Task]:
    """
    Get all completed tasks for a specific user.
    """
    statement = select(Task).where(Task.user_id == user_id, Task.status == True)
    result = await db_session.exec(statement)
    completed_tasks = result.all()

    return completed_tasks

async def get_pending_tasks_for_user(*, db_session: AsyncSession, user_id: str) -> List[Task]:
    """
    Get all pending tasks for a specific user.
    """
    statement = select(Task).where(Task.user_id == user_id, Task.status == False)
    result = await db_session.exec(statement)
    pending_tasks = result.all()

    return pending_tasks

async def get_dashboard_stats_for_user(*, db_session: AsyncSession, user_id: str) -> Dict[str, int]:
    """
    Get dashboard statistics for a specific user in a single efficient query.
    Returns total tasks, completed tasks, and pending tasks counts.
    """
    print('--- Fetching Stats ---')
    from sqlalchemy import func, case

    # Efficiently count total and completed tasks in one query
    statement = select(
        func.count(Task.id),
        func.sum(case((Task.status == True, 1), else_=0))
    ).where(Task.user_id == user_id)

    result = await db_session.exec(statement)
    total_count, completed_count = result.one() or (0, 0)

    # Fix Stats Logic: Ensure counts are explicitly cast to int to prevent NoneType errors
    total_count = int(total_count) if total_count is not None else 0
    completed_count = int(completed_count) if completed_count is not None else 0

    pending_count = total_count - completed_count

    return {
        "total_tasks": total_count,
        "completed_tasks": completed_count,
        "pending_tasks": pending_count,
    }