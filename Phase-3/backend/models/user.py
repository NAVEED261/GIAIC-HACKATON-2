"""
User Model

Represents a user in the todo system.
Implements @specs/phase-3-overview.md - Authentication

@author: Phase-3 System
@created: 2025-12-18
"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from passlib.context import CryptContext

if TYPE_CHECKING:
    from .task import Task

# Password hashing context - use argon2 as fallback if bcrypt has issues
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:
    # Fallback to argon2 if bcrypt fails
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class User(SQLModel, table=True):
    """User database model for persistence"""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100, min_length=1)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        """Verify a password against the hashed password"""
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)


class UserCreate(SQLModel):
    """Schema for user registration"""
    email: str = Field(max_length=255)
    name: str = Field(max_length=100, min_length=1)
    password: str = Field(min_length=8, max_length=100)


class UserRead(SQLModel):
    """Schema for reading a user (response)"""
    id: int
    email: str
    name: str
    created_at: datetime


class UserLogin(SQLModel):
    """Schema for user login"""
    email: str = Field(max_length=255)
    password: str = Field(max_length=100)
