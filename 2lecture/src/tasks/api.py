from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_db
from src.tasks.exceptions import (TaskNotFoundException, TaskValidationException,
                              raise_http_exception)
from src.tasks.models import Task, TaskCreate, TaskUpdate
from src.tasks.service import TaskService
from .example import add

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[Task])
async def get_tasks(db: AsyncSession = Depends(get_async_db)):
    """Get all tasks."""
    try:
        tasks = await TaskService.get_all_tasks(db)
        return [
            Task(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
    except Exception as e:
        raise_http_exception(e)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    """Get a specific task by ID."""
    try:
        task = await TaskService.get_task_by_id(task_id, db)
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except (TaskNotFoundException,) as e:
        raise_http_exception(e)


@router.post("/", response_model=Task)
async def create_task(
    task_data: TaskCreate = Body(...),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new task."""
    try:
        task = await TaskService.create_task(task_data, db)
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except TaskValidationException as e:
        raise_http_exception(e)


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_data: TaskUpdate = Body(...),
    db: AsyncSession = Depends(get_async_db)
):
    """Update an existing task."""
    try:
        task = await TaskService.update_task(task_id, task_data, db)
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except (TaskNotFoundException, TaskValidationException) as e:
        raise_http_exception(e)


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    """Delete a task."""
    try:
        await TaskService.delete_task(task_id, db)
        return {"message": "Task deleted successfully"}
    except TaskNotFoundException as e:
        raise_http_exception(e)


@router.post("/test-celery/{x}/{y}")
async def test_celery(x: int, y: int):
    """
    Test endpoint for Celery task
    """
    # Send the task to Celery
    task = add.delay(x, y)
    
    return {
        "message": "Task sent to Celery",
        "task_id": task.id,
        "status": "processing"
    }


@router.get("/task-result/{task_id}")
async def get_task_result(task_id: str):
    """
    Get the result of a Celery task
    """
    task = add.AsyncResult(task_id)
    
    if task.ready():
        return {
            "status": "completed",
            "result": task.get()
        }
    return {
        "status": "processing"
    }
