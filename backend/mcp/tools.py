"""
MCP tools for chatbot backend.
These tools provide the interface between the AI agent and the task management system.
"""

import asyncio
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import Session, select
from models.task import Task, PriorityEnum
from models.user import User
from services.task_service import create_task, get_tasks_by_user, get_task_by_id, update_task, delete_task
from mcp.config import config


class MCPTaskTools:
    """
    MCP tools for task operations.
    These tools are stateless and query the database directly.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

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
        try:
            # Validate priority
            if priority and priority not in ["high", "medium", "low"]:
                raise ValueError(f"Invalid priority: {priority}. Must be one of: high, medium, low")

            # Parse due date if provided
            parsed_due_date = None
            if due_date:
                from datetime import datetime
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

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

            return {
                "success": True,
                "task": {
                    "id": str(created_task.id),
                    "title": created_task.title,
                    "description": created_task.description,
                    "priority": created_task.priority.value,
                    "due_date": created_task.due_date.isoformat() if created_task.due_date else None,
                    "completed": created_task.completed,
                    "user_id": str(created_task.user_id),
                    "created_at": created_task.created_at.isoformat(),
                    "updated_at": created_task.updated_at.isoformat()
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

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
        try:
            # Build query to get tasks for the user
            query = select(Task).where(Task.user_id == user_id)

            # Apply status filter if specified
            if status and status != "all":
                if status == "pending":
                    query = query.where(Task.completed == False)
                elif status == "completed":
                    query = query.where(Task.completed == True)

            # Execute query
            tasks = self.db_session.exec(query).all()

            # Convert tasks to dictionaries
            task_list = []
            for task in tasks:
                task_dict = {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority.value,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "completed": task.completed,
                    "user_id": str(task.user_id),
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                task_list.append(task_dict)

            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

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
        try:
            # Verify that the task belongs to the user
            task = self.db_session.get(Task, UUID(task_id))
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

            # Update the task to completed
            task.completed = True
            task.updated_at = datetime.utcnow()
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority.value,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "completed": task.completed,
                    "user_id": str(task.user_id),
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

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
        try:
            # Verify that the task belongs to the user
            task = self.db_session.get(Task, UUID(task_id))
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

            # Delete the task
            self.db_session.delete(task)
            self.db_session.commit()

            return {
                "success": True,
                "message": "Task deleted successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

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
        try:
            # Validate priority if provided
            if priority and priority not in ["high", "medium", "low"]:
                raise ValueError(f"Invalid priority: {priority}. Must be one of: high, medium, low")

            # Verify that the task belongs to the user
            task = self.db_session.get(Task, UUID(task_id))
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
                from datetime import datetime
                parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                task.due_date = parsed_due_date
            if completed is not None:
                task.completed = completed

            task.updated_at = datetime.utcnow()
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority.value,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "completed": task.completed,
                    "user_id": str(task.user_id),
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Helper function to create tools with a session
def create_mcp_tools(db_session: Session) -> MCPTaskTools:
    """
    Factory function to create MCP task tools with a database session.

    Args:
        db_session: The database session to use

    Returns:
        MCPTaskTools instance
    """
    return MCPTaskTools(db_session)