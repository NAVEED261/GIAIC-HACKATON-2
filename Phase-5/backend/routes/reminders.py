"""
Reminder Routes - Phase-5
API endpoints for reminder management

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime
from sqlmodel import Session

from models.reminder import (
    Reminder, ReminderCreate, ReminderRead, ReminderUpdate, ReminderSnooze
)
from services.reminder_service import ReminderService
from db import get_session
from middleware.auth import get_current_user

router = APIRouter(prefix="/reminders", tags=["Reminders"])


def get_reminder_service(session: Session = Depends(get_session)) -> ReminderService:
    return ReminderService(session)


@router.post("/", response_model=ReminderRead, status_code=201)
async def create_reminder(
    reminder_data: ReminderCreate,
    current_user = Depends(get_current_user),
    service: ReminderService = Depends(get_reminder_service)
):
    """Create a new reminder for a task"""
    reminder = await service.create_reminder(
        task_id=reminder_data.task_id,
        user_id=current_user.id,
        remind_at=reminder_data.remind_at,
        reminder_type=reminder_data.reminder_type,
        message=reminder_data.message
    )
    return reminder


@router.get("/", response_model=List[ReminderRead])
async def get_reminders(
    days_ahead: int = Query(7, ge=1, le=90),
    current_user = Depends(get_current_user),
    service: ReminderService = Depends(get_reminder_service)
):
    """Get upcoming reminders"""
    return service.get_upcoming_reminders(current_user.id, days_ahead)


@router.get("/overdue", response_model=List[dict])
async def get_overdue_tasks(
    current_user = Depends(get_current_user),
    service: ReminderService = Depends(get_reminder_service)
):
    """Get all overdue tasks"""
    tasks = service.get_overdue_tasks(current_user.id)
    return [
        {
            "id": t.id,
            "title": t.title,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "priority": t.priority.value,
            "days_overdue": (datetime.utcnow() - t.due_date).days if t.due_date else 0
        }
        for t in tasks
    ]


@router.get("/due-today", response_model=List[dict])
async def get_tasks_due_today(
    current_user = Depends(get_current_user),
    service: ReminderService = Depends(get_reminder_service)
):
    """Get tasks due today"""
    tasks = service.get_due_today(current_user.id)
    return [
        {
            "id": t.id,
            "title": t.title,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "priority": t.priority.value
        }
        for t in tasks
    ]


@router.get("/{reminder_id}", response_model=ReminderRead)
async def get_reminder(
    reminder_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a single reminder"""
    reminder = session.get(Reminder, reminder_id)
    if not reminder or reminder.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder


@router.patch("/{reminder_id}", response_model=ReminderRead)
async def update_reminder(
    reminder_id: int,
    reminder_data: ReminderUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a reminder"""
    reminder = session.get(Reminder, reminder_id)
    if not reminder or reminder.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reminder not found")

    update_data = reminder_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reminder, key, value)

    reminder.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(reminder)
    return reminder


@router.delete("/{reminder_id}", status_code=204)
async def cancel_reminder(
    reminder_id: int,
    current_user = Depends(get_current_user),
    service: ReminderService = Depends(get_reminder_service)
):
    """Cancel a reminder"""
    result = await service.cancel_reminder(reminder_id, current_user.id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])


@router.post("/{reminder_id}/snooze", response_model=dict)
async def snooze_reminder(
    reminder_id: int,
    snooze_data: ReminderSnooze,
    current_user = Depends(get_current_user),
    service: ReminderService = Depends(get_reminder_service)
):
    """Snooze a reminder"""
    result = await service.snooze_reminder(
        reminder_id,
        current_user.id,
        snooze_data.snooze_minutes
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ==================== Dapr Integration Endpoints ====================

@router.post("/process-due", response_model=List[dict])
async def process_due_reminders(
    service: ReminderService = Depends(get_reminder_service)
):
    """
    Process all due reminders

    This endpoint is called by Dapr cron binding.
    Internal use only.
    """
    return await service.process_due_reminders()
