"""
Task Routes - Phase-5
API endpoints for task management with advanced features

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session

from models.task import (
    Task, TaskCreate, TaskRead, TaskUpdate, TaskFilter, Priority
)
from services.task_service import TaskService
from services.recurring_service import RecurringTaskService
from db import get_session
from middleware.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    return TaskService(session)


def get_recurring_service(session: Session = Depends(get_session)) -> RecurringTaskService:
    return RecurringTaskService(session)


@router.post("/", response_model=TaskRead, status_code=201)
async def create_task(
    task_data: TaskCreate,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    task = await service.create_task(current_user.id, task_data)
    return task


@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    status: Optional[str] = Query(None, description="completed/pending/all"),
    priority: Optional[Priority] = Query(None),
    is_recurring: Optional[bool] = Query(None),
    has_due_date: Optional[bool] = Query(None),
    is_overdue: Optional[bool] = Query(None),
    tag_ids: Optional[str] = Query(None, description="Comma-separated tag IDs"),
    search: Optional[str] = Query(None, description="Search in title/description"),
    sort_by: Optional[str] = Query("created_at", description="created_at/due_date/priority/title"),
    sort_order: Optional[str] = Query("desc", description="asc/desc"),
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Get tasks with filtering and sorting"""
    filter_params = TaskFilter(
        status=status,
        priority=priority,
        is_recurring=is_recurring,
        has_due_date=has_due_date,
        is_overdue=is_overdue,
        tag_ids=[int(x) for x in tag_ids.split(",")] if tag_ids else None,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return service.get_tasks(current_user.id, filter_params)


@router.get("/statistics")
async def get_task_statistics(
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Get task statistics"""
    return service.get_statistics(current_user.id)


@router.get("/overdue", response_model=List[TaskRead])
async def get_overdue_tasks(
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Get all overdue tasks"""
    filter_params = TaskFilter(is_overdue=True)
    return service.get_tasks(current_user.id, filter_params)


@router.get("/due-today", response_model=List[TaskRead])
async def get_tasks_due_today(
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get tasks due today"""
    from services.reminder_service import ReminderService
    reminder_service = ReminderService(session)
    return reminder_service.get_due_today(current_user.id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Get a single task"""
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Update a task"""
    task = await service.update_task(task_id, current_user.id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Delete a task"""
    success = await service.delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/complete", response_model=TaskRead)
async def complete_task(
    task_id: int,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
    recurring_service: RecurringTaskService = Depends(get_recurring_service)
):
    """Complete a task (handles recurring tasks automatically)"""
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.is_recurring:
        result = await recurring_service.complete_recurring_task(task_id)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return service.get_task(result["new_task_id"], current_user.id)
    else:
        task_update = TaskUpdate(completed=True)
        return await service.update_task(task_id, current_user.id, task_update)


@router.post("/{task_id}/priority", response_model=TaskRead)
async def set_task_priority(
    task_id: int,
    priority: Priority,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Set task priority"""
    task = await service.set_priority(task_id, current_user.id, priority)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/due-date", response_model=TaskRead)
async def set_task_due_date(
    task_id: int,
    due_date: Optional[datetime] = None,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Set task due date"""
    task = await service.set_due_date(task_id, current_user.id, due_date)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/tags", response_model=TaskRead)
async def add_tags_to_task(
    task_id: int,
    tag_ids: List[int],
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Add tags to a task"""
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await service.add_tags(task_id, tag_ids)
    return service.get_task(task_id, current_user.id)


@router.delete("/{task_id}/tags", response_model=TaskRead)
async def remove_tags_from_task(
    task_id: int,
    tag_ids: List[int],
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    """Remove tags from a task"""
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await service.remove_tags(task_id, tag_ids)
    return service.get_task(task_id, current_user.id)


# ==================== Recurring Task Endpoints ====================

@router.post("/{task_id}/skip", response_model=dict)
async def skip_recurring_occurrence(
    task_id: int,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
    recurring_service: RecurringTaskService = Depends(get_recurring_service)
):
    """Skip the next occurrence of a recurring task"""
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    result = await recurring_service.skip_occurrence(task_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{task_id}/stop-recurring", response_model=dict)
async def stop_recurring_task(
    task_id: int,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
    recurring_service: RecurringTaskService = Depends(get_recurring_service)
):
    """Stop a recurring task series"""
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    result = await recurring_service.stop_recurring(task_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{task_id}/series", response_model=List[TaskRead])
async def get_recurring_series(
    task_id: int,
    current_user = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
    recurring_service: RecurringTaskService = Depends(get_recurring_service)
):
    """Get all instances of a recurring task series"""
    task = service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return recurring_service.get_recurring_series(task_id)
