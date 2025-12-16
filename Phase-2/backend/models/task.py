"""
Task Model - SQLModel definition for Task entity
Phase-2: Backend Agent - Database Agent collaboration
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict


class Task(SQLModel, table=True):
    """
    Task entity for todo management with user isolation.

    Attributes:
        id: Auto-increment task identifier
        user_id: Foreign key to User (cascade delete)
        title: Task title (required, 1-200 chars)
        description: Detailed task description (optional, max 1000 chars)
        status: Task status - "Pending" or "Completed" (default: "Pending")
        priority: Task priority - "Low", "Medium", "High" (default: "Medium")
        created_at: Task creation timestamp (auto-set)
        updated_at: Last update timestamp (auto-set)
        completed_at: Task completion timestamp (optional, nullable)
        deleted_at: Soft delete timestamp (optional, nullable)
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True, description="Auto-increment task ID")

    # Foreign Key (User relationship)
    user_id: str = Field(foreign_key="user.id", description="User who owns this task")

    # Required Fields
    title: str = Field(
        min_length=1,
        max_length=200,
        index=True,
        description="Task title (1-200 characters)"
    )

    # Optional Fields
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Detailed task description (max 1000 characters)"
    )

    # Status Fields
    status: str = Field(
        default="Pending",
        description="Task status: 'Pending' or 'Completed'",
        index=True
    )

    priority: str = Field(
        default="Medium",
        description="Task priority: 'Low', 'Medium', or 'High'"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Task creation timestamp"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    completed_at: Optional[datetime] = Field(
        default=None,
        description="Task completion timestamp (set when status=Completed)"
    )

    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Soft delete timestamp (for soft deletes)"
    )


class TaskResponse(SQLModel):
    """
    Response schema for task data in API responses
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None


class TaskCreate(SQLModel):
    """Request schema for creating a task"""
    title: str = Field(min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description"
    )
    priority: str = Field(default="Medium", description="Task priority")


class TaskUpdate(SQLModel):
    """Request schema for updating a task"""
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[str] = Field(default=None, description="'Pending' or 'Completed'")
    priority: Optional[str] = Field(default=None)
