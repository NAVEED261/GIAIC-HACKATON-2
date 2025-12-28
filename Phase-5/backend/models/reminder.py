"""
Reminder Model - Phase-5
Task reminders and notifications

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class ReminderType(str, Enum):
    """Reminder notification types"""
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    IN_APP = "in_app"


class ReminderStatus(str, Enum):
    """Reminder status"""
    PENDING = "pending"
    SENT = "sent"
    SNOOZED = "snoozed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class Reminder(SQLModel, table=True):
    """
    Reminder database model

    Used for scheduling task reminders.
    Integrated with Dapr cron binding for scheduling.
    """

    __tablename__ = "reminders"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(index=True, foreign_key="tasks.id")
    user_id: int = Field(index=True, foreign_key="users.id")

    # Reminder details
    remind_at: datetime = Field(index=True)
    reminder_type: ReminderType = Field(default=ReminderType.PUSH)
    message: Optional[str] = Field(default=None, max_length=500)

    # Status tracking
    status: ReminderStatus = Field(default=ReminderStatus.PENDING, index=True)
    sent_at: Optional[datetime] = Field(default=None)
    snoozed_until: Optional[datetime] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Optional["Task"] = Relationship(back_populates="reminders")
    user: Optional["User"] = Relationship(back_populates="reminders")


class ReminderCreate(SQLModel):
    """Schema for creating a reminder"""
    task_id: int
    remind_at: datetime
    reminder_type: ReminderType = ReminderType.PUSH
    message: Optional[str] = Field(default=None, max_length=500)


class ReminderRead(SQLModel):
    """Schema for reading a reminder"""
    id: int
    task_id: int
    user_id: int
    remind_at: datetime
    reminder_type: ReminderType
    message: Optional[str]
    status: ReminderStatus
    sent_at: Optional[datetime]
    snoozed_until: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ReminderUpdate(SQLModel):
    """Schema for updating a reminder"""
    remind_at: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None
    message: Optional[str] = Field(default=None, max_length=500)
    status: Optional[ReminderStatus] = None


class ReminderSnooze(SQLModel):
    """Schema for snoozing a reminder"""
    snooze_minutes: int = Field(default=15, ge=5, le=1440)  # 5 min to 24 hours
