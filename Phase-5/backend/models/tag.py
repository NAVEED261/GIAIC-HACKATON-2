"""
Tag Model - Phase-5
Task categorization and labeling

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class TaskTag(SQLModel, table=True):
    """Junction table for Task-Tag many-to-many relationship"""

    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Tag(SQLModel, table=True):
    """
    Tag database model

    Used for categorizing and labeling tasks.
    Each user has their own set of tags.
    """

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="users.id")
    name: str = Field(max_length=50, min_length=1)
    color: str = Field(default="#3B82F6", max_length=7)  # Hex color
    description: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships - commented to avoid circular import issues
    # user: Optional["User"] = Relationship(back_populates="tags")
    # tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTag)


class TagCreate(SQLModel):
    """Schema for creating a tag"""
    name: str = Field(min_length=1, max_length=50)
    color: str = Field(default="#3B82F6", max_length=7)
    description: Optional[str] = Field(default=None, max_length=200)


class TagRead(SQLModel):
    """Schema for reading a tag"""
    id: int
    user_id: int
    name: str
    color: str
    description: Optional[str]
    created_at: datetime
    task_count: int = 0

    class Config:
        from_attributes = True


class TagUpdate(SQLModel):
    """Schema for updating a tag"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    color: Optional[str] = Field(default=None, max_length=7)
    description: Optional[str] = Field(default=None, max_length=200)
