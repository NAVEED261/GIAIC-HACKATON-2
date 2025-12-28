"""
Task Model - Phase-5 Enhanced
Advanced features: Priority, Due Date, Recurring, Tags

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag, TaskTag
    from .reminder import Reminder


class Priority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class RecurrencePattern(str, Enum):
    """Recurrence pattern types"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class Task(SQLModel, table=True):
    """
    Task database model - Phase-5 Enhanced

    New fields:
    - priority: Task priority level
    - due_date: Task due date/time
    - is_recurring: Whether task repeats
    - recurrence_pattern: How it repeats (daily/weekly/monthly)
    - recurrence_interval: Every N days/weeks/months
    - parent_task_id: For recurring task instances
    - next_occurrence: Next scheduled occurrence
    """

    __tablename__ = "tasks"

    # Core fields (from Phase-3)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="users.id")
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Phase-5: Priority
    priority: Priority = Field(default=Priority.MEDIUM, index=True)

    # Phase-5: Due Date
    due_date: Optional[datetime] = Field(default=None, index=True)

    # Phase-5: Recurring Tasks
    is_recurring: bool = Field(default=False, index=True)
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None)
    recurrence_interval: int = Field(default=1)  # Every N units
    parent_task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")
    next_occurrence: Optional[datetime] = Field(default=None)

    # Relationships - defined after all models are loaded
    # user: Optional["User"] = Relationship(back_populates="tasks")
    # tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
    # reminders: List["Reminder"] = Relationship(back_populates="task")


class TaskCreate(SQLModel):
    """Schema for creating a task"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[Priority] = Field(default=Priority.MEDIUM)
    due_date: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[RecurrencePattern] = None
    recurrence_interval: int = 1
    tag_ids: Optional[List[int]] = None


class TaskRead(SQLModel):
    """Schema for reading a task (response)"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    due_date: Optional[datetime]
    is_recurring: bool
    recurrence_pattern: Optional[RecurrencePattern]
    recurrence_interval: int
    parent_task_id: Optional[int]
    next_occurrence: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    # tags will be loaded separately via API
    is_overdue: bool = False

    class Config:
        from_attributes = True


class TaskUpdate(SQLModel):
    """Schema for updating a task (partial updates)"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    recurrence_interval: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class TaskFilter(SQLModel):
    """Schema for filtering tasks"""
    status: Optional[str] = None  # completed, pending, all
    priority: Optional[Priority] = None
    is_recurring: Optional[bool] = None
    has_due_date: Optional[bool] = None
    is_overdue: Optional[bool] = None
    tag_ids: Optional[List[int]] = None
    search: Optional[str] = None  # Full-text search
    sort_by: Optional[str] = "created_at"  # created_at, due_date, priority, title
    sort_order: Optional[str] = "desc"  # asc, desc


# Forward reference for TagRead
from .tag import TagRead
TaskRead.model_rebuild()
