"""
Conversation Model - Phase-5
Stores chat conversations for history
"""

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    """Conversation model for chat history"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")
