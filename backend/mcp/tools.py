"""
MCP tools for chatbot backend.
These tools provide the interface between the AI agent and the task management system.
"""

import asyncio
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime, date
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.task import Task, PriorityEnum
from models.user import User
from services.task_service import create_task, get_tasks_by_user, get_task_by_id, update_task, delete_task
from mcp.config import config


class MCPTaskTools:
    """
    MCP tools for task operations.
    These tools are stateless and query the database directly.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        # Verify session type on init as required by skill file
        print(f"✅ Tools initialized with {type(db_session)}")

    async def add_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        priority: Optional[str] = "medium",  # Default to "medium" priority
        due_date: Optional[str] = None  # Expected in ISO 8601 format (YYYY-MM-DD)
    ) -> Dict[str, Any]:
        """
        Add a new task for the specified user.

        Args:
            user_id: The ID of the user creating the task
            title: The title of the task
            description: Optional description of the task
            priority: Priority level ("high", "medium", "low") - defaults to "medium"
            due_date: Due date in ISO 8601 format (YYYY-MM-DD) - optional

        Returns:
            Dict containing the created task data
        """
        # Add logging as required by skill file
        print(f"✅ add_task executing for user {user_id}")
        print(f"✅ Tool add_task called with user_id={user_id}, title={title}")

        import traceback

        try:
            # Validate priority
            if priority and priority not in ["high", "medium", "low"]:
                raise ValueError(f"Invalid priority: {priority}. Must be one of: high, medium, low")

            # Parse due date - default to today's date if not provided
            parsed_due_date = None
            if due_date:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            else:
                # Default to today's date as per ID & Date Fix requirement
                parsed_due_date = date.today()  # Use dynamic date to match system message

            # Create the task using the task service
            task_data = {
                "title": title,
                "description": description,
                "priority": PriorityEnum.MEDIUM if priority == "medium" else (PriorityEnum.HIGH if priority == "high" else PriorityEnum.LOW) if priority else PriorityEnum.MEDIUM,
                "due_date": parsed_due_date,
                "user_id": user_id
            }

            from sqlmodel import SQLModel
            from models.task import TaskCreate
            # Create TaskCreate object from task_data
            task_create_obj = TaskCreate(**{
                'title': task_data['title'],
                'description': task_data['description'],
                'priority': task_data['priority'],
                'due_date': task_data['due_date']
            })

            # Call the create_task function directly
            created_task = await create_task(db_session=self.db_session, task_in=task_create_obj, user_id=task_data['user_id'])

            # Handle date serialization safely as per Task Serialization Safety
            due_date_str = created_task.due_date.strftime('%Y-%m-%d') if created_task.due_date else None

            result_task = {
                "id": str(created_task.id),
                "title": created_task.title,
                "description": created_task.description,
                "priority": created_task.priority.value,
                "due_date": due_date_str,
                "completed": created_task.status,
                "user_id": str(created_task.user_id),
                "created_at": created_task.created_at.isoformat(),
                "updated_at": created_task.updated_at.isoformat()
            }

            # Log before returning as required by skill file
            print(f"✅ Processing {created_task.id}")
            print(f"✅ Returning task with {len(result_task)} fields")

            return {
                "success": True,
                "task": result_task
            }

        except Exception as e:
            # Log error type and message as required by skill file
            print(f"❌ add_task ERROR: {type(e).__name__}: {e}")
            # Log full traceback as required by skill file
            traceback.print_exc()
            # Never swallow exceptions - always re-raise after logging
            raise

    async def list_tasks(
        self,
        user_id: str,
        status: Optional[str] = None  # "all", "pending", "completed" - defaults to "all"
    ) -> Dict[str, Any]:
        """
        List tasks for the specified user with optional status filtering.

        Args:
            user_id: The ID of the user whose tasks to retrieve
            status: Status filter ("all", "pending", "completed") - defaults to "all"

        Returns:
            Dict containing the list of tasks
        """
        # Add logging as required by skill file
        print(f"✅ list_tasks executing for user {user_id}")
        print(f"✅ Tool list_tasks called with user_id={user_id}, status={status}")

        import traceback

        try:
            # Build query to get tasks for the user
            query = select(Task).where(Task.user_id == user_id)

            # Apply status filter if specified
            if status and status != "all":
                if status == "pending":
                    query = query.where(Task.status == False)
                elif status == "completed":
                    query = query.where(Task.status == True)

            # Execute query asynchronously
            result = await self.db_session.exec(query)
            tasks = result.all()

            # Log result count as required by skill file
            print(f"✅ Found {len(tasks)} items")

            # Convert tasks to dictionaries
            task_list = []
            for task in tasks:
                # Log each item as required by skill file
                print(f"✅ Processing {task.id}")

                # Handle date serialization safely as per Task Serialization Safety
                due_date_str = task.due_date.strftime('%Y-%m-%d') if task.due_date else None

                task_dict = {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority.value,
                    "due_date": due_date_str,  # Changed from "None" to None for consistency
                    "completed": task.status,
                    "user_id": str(task.user_id),
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                task_list.append(task_dict)

            # Log before returning as required by skill file
            print(f"✅ Returning {len(task_list)} tasks")

            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list)
            }

        except Exception as e:
            # Log error type and message as required by skill file
            print(f"❌ list_tasks ERROR: {type(e).__name__}: {e}")
            # Log full traceback as required by skill file
            traceback.print_exc()
            # Never swallow exceptions - always re-raise after logging
            raise

    async def complete_task(
        self,
        user_id: str,
        task_id: str
    ) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to complete

        Returns:
            Dict containing the updated task data
        """
        # Add logging as required by skill file
        print(f"✅ complete_task executing for user {user_id}")
        print(f"✅ Tool complete_task called with user_id={user_id}, task_id={task_id}")

        import traceback

        try:
            # Handle task ID conversion as required by skill file (Task IDs may be strings or ints)
            try:
                actual_task_id = int(task_id) if task_id.isdigit() else task_id
            except ValueError:
                actual_task_id = task_id  # fallback to original if conversion fails

            # Verify that the task belongs to the user
            task = await self.db_session.get(Task, actual_task_id)
            if not task:
                # This is an expected business logic error, return appropriate response
                return {
                    "success": False,
                    "error": "Task not found"
                }

            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Access denied: You don't have permission to modify this task"
                }

            # Update the task to completed
            task.status = True
            task.updated_at = datetime.utcnow()
            self.db_session.add(task)
            await self.db_session.commit()
            await self.db_session.refresh(task)

            # Handle date serialization safely as per Task Serialization Safety
            due_date_str = task.due_date.strftime('%Y-%m-%d') if task.due_date else None

            result_task = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "due_date": due_date_str,
                "completed": task.status,
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }

            # Log before returning as required by skill file
            print(f"✅ Processing {task.id}")
            print(f"✅ Returning task with {len(result_task)} fields")

            return {
                "success": True,
                "task": result_task
            }

        except Exception as e:
            # Log error type and message as required by skill file
            print(f"❌ complete_task ERROR: {type(e).__name__}: {e}")
            # Log full traceback as required by skill file
            traceback.print_exc()
            # Never swallow exceptions - always re-raise after logging
            raise

    async def delete_task(
        self,
        user_id: str,
        task_id: str
    ) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to delete

        Returns:
            Dict indicating success or failure
        """
        # Add logging as required by skill file
        print(f"✅ delete_task executing for user {user_id}")
        print(f"✅ Tool delete_task called with user_id={user_id}, task_id={task_id}")

        import traceback

        try:
            # Handle task ID conversion as required by skill file (Task IDs may be strings or ints)
            try:
                actual_task_id = int(task_id) if task_id.isdigit() else task_id
            except ValueError:
                actual_task_id = task_id  # fallback to original if conversion fails

            # Verify that the task belongs to the user
            task = await self.db_session.get(Task, actual_task_id)
            if not task:
                return {
                    "success": False,
                    "error": "Task not found"
                }

            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Access denied: You don't have permission to delete this task"
                }

            # Verify the task exists and get its ID before deletion
            task_id_before_delete = task.id
            print(f"🔥 About to delete task with ID: {task_id_before_delete}")
            print(f"🔥 Task object: {task}")

            # Delete the task from the session
            await self.db_session.delete(task)
            print(f"🔥 Task {task_id_before_delete} marked for deletion")

            # Commit the transaction to persist the deletion
            await self.db_session.commit()
            print(f"🔥 Transaction committed, task {task_id_before_delete} should be permanently deleted")

            # Optionally, verify the task is gone by attempting to query it again
            try:
                verification_task = await self.db_session.get(Task, task_id_before_delete)
                if verification_task is None:
                    print(f"🔥 Verification: Task {task_id_before_delete} confirmed deleted from DB")
                else:
                    print(f"⚠️  Warning: Task {task_id_before_delete} still exists in DB after deletion attempt")
            except Exception as verification_error:
                print(f"⚠️  Verification error: {verification_error}")

            # Log before returning as required by skill file
            print(f"✅ Processing {task_id_before_delete}")
            print(f"✅ Task {task_id_before_delete} deleted successfully")

            return {
                "success": True,
                "message": "Task deleted successfully"
            }

        except Exception as e:
            # Log error type and message as required by skill file
            print(f"❌ delete_task ERROR: {type(e).__name__}: {e}")
            # Log full traceback as required by skill file
            traceback.print_exc()
            # Never swallow exceptions - always re-raise after logging
            raise

    async def update_task(
        self,
        user_id: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update a task with the provided fields.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to update
            title: Optional new title
            description: Optional new description
            priority: Optional new priority ("high", "medium", "low")
            due_date: Optional new due date in ISO 8601 format (YYYY-MM-DD)
            completed: Optional new completion status

        Returns:
            Dict containing the updated task data
        """
        # Add logging as required by skill file
        print(f"✅ update_task executing for user {user_id}")
        print(f"✅ Tool update_task called with user_id={user_id}, task_id={task_id}")

        import traceback

        try:
            # Validate priority if provided
            if priority and priority not in ["high", "medium", "low"]:
                raise ValueError(f"Invalid priority: {priority}. Must be one of: high, medium, low")

            # Handle task ID conversion as required by skill file (Task IDs may be strings or ints)
            try:
                actual_task_id = int(task_id) if task_id.isdigit() else task_id
            except ValueError:
                actual_task_id = task_id  # fallback to original if conversion fails

            # Verify that the task belongs to the user
            task = await self.db_session.get(Task, actual_task_id)
            if not task:
                return {
                    "success": False,
                    "error": "Task not found"
                }

            if str(task.user_id) != user_id:
                return {
                    "success": False,
                    "error": "Access denied: You don't have permission to modify this task"
                }

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = PriorityEnum.MEDIUM if priority == "medium" else (PriorityEnum.HIGH if priority == "high" else PriorityEnum.LOW)
            if due_date is not None:
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                task.due_date = parsed_due_date
            if completed is not None:
                task.status = completed

            task.updated_at = datetime.utcnow()
            self.db_session.add(task)
            await self.db_session.commit()
            await self.db_session.refresh(task)

            # Handle date serialization safely as per Task Serialization Safety
            due_date_str = task.due_date.strftime('%Y-%m-%d') if task.due_date else None

            result_task = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "due_date": due_date_str,
                "completed": task.status,
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }

            # Log before returning as required by skill file
            print(f"✅ Processing {task.id}")
            print(f"✅ Returning task with {len(result_task)} fields")

            return {
                "success": True,
                "task": result_task
            }

        except Exception as e:
            # Log error type and message as required by skill file
            print(f"❌ update_task ERROR: {type(e).__name__}: {e}")
            # Log full traceback as required by skill file
            traceback.print_exc()
            # Never swallow exceptions - always re-raise after logging
            raise


# Helper function to create tools with a session
def create_mcp_tools(db_session: AsyncSession) -> MCPTaskTools:
    """
    Factory function to create MCP task tools with a database session.

    Args:
        db_session: The database session to use

    Returns:
        MCPTaskTools instance
    """
    return MCPTaskTools(db_session)