"""
Task service layer containing business logic for task operations.
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.crud import TaskDAO
from src.tasks.exceptions import TaskNotFoundException, TaskValidationException
from src.tasks.models import TaskCreate, TaskUpdate
from src.tasks.schema import Task as DBTask


class TaskService:

    @staticmethod
    async def get_all_tasks(db: AsyncSession) -> List[DBTask]:
        """Get all tasks."""
        return await TaskDAO.get_all(db)

    @staticmethod
    async def get_task_by_id(task_id: int, db: AsyncSession) -> DBTask:
        """Get task by ID."""
        task = await TaskDAO.get_by_id(task_id, db)
        if not task:
            raise TaskNotFoundException(task_id)
        return task

    @staticmethod
    async def create_task(task_data: TaskCreate, db: AsyncSession) -> DBTask:
        """Create a new task."""
        if not task_data.title:
            raise TaskValidationException("Title is required")
        return await TaskDAO.create(task_data, db)

    @staticmethod
    async def update_task(
        task_id: int, 
        task_data: TaskUpdate, 
        db: AsyncSession
    ) -> DBTask:
        """Update an existing task."""
        task = await TaskDAO.get_by_id(task_id, db)
        if not task:
            raise TaskNotFoundException(task_id)
        return await TaskDAO.update(task_id, task_data, db)

    @staticmethod
    async def delete_task(task_id: int, db: AsyncSession) -> bool:
        """Delete a task."""
        task = await TaskDAO.get_by_id(task_id, db)
        if not task:
            raise TaskNotFoundException(task_id)
        await TaskDAO.delete(task_id, db)
        return True 