"""
Database Models - Phase-5

All SQLModel entities for Phase-5 advanced features:
- Task (with priority, due_date, recurring)
- Tag (categorization)
- Reminder (notifications)
- User (with preferences)

@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from .task import (
    Task, TaskCreate, TaskRead, TaskUpdate, TaskFilter,
    Priority, RecurrencePattern
)
from .tag import Tag, TagCreate, TagRead, TagUpdate, TaskTag
from .reminder import (
    Reminder, ReminderCreate, ReminderRead, ReminderUpdate, ReminderSnooze,
    ReminderType, ReminderStatus
)
from .user import User, UserCreate, UserRead, UserLogin, ReminderPreferences
from .conversation import Conversation
from .message import Message

__all__ = [
    # Task
    "Task",
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    "TaskFilter",
    "Priority",
    "RecurrencePattern",

    # Tag
    "Tag",
    "TagCreate",
    "TagRead",
    "TagUpdate",
    "TaskTag",

    # Reminder
    "Reminder",
    "ReminderCreate",
    "ReminderRead",
    "ReminderUpdate",
    "ReminderSnooze",
    "ReminderType",
    "ReminderStatus",

    # User
    "User",
    "UserCreate",
    "UserRead",
    "UserLogin",
    "ReminderPreferences",

    # Chat History
    "Conversation",
    "Message",
]
