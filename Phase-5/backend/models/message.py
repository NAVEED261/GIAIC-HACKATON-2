"""
Message Model - Phase-5
Stores individual chat messages
"""

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """Message model for chat history"""

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(index=True)
    role: str = Field(index=True)  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
