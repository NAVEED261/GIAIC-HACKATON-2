"""
User Model - SQLModel definition for User entity
Phase-2: Backend Agent - Database Agent collaboration
"""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, ConfigDict


class User(SQLModel, table=True):
    """
    User entity for authentication and multi-user isolation.

    Attributes:
        id: Unique user identifier (UUID or similar string)
        email: User email address (unique, required)
        name: User full name (required)
        password_hash: Bcrypt hashed password (required)
        created_at: Account creation timestamp (auto-set)
        updated_at: Last update timestamp (auto-set)
        is_active: Account active status (default: True)
        last_login_at: Last login timestamp (optional, nullable)
    """

    model_config = ConfigDict(from_attributes=True)

    # Primary Key
    id: str | None = Field(default=None, primary_key=True, description="Unique user identifier")

    # Required Fields
    email: EmailStr = Field(unique=True, index=True, description="User email (unique)")
    name: str = Field(min_length=1, max_length=255, description="User full name")
    password_hash: str = Field(description="Bcrypt hashed password")

    # Timestamps with defaults
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    # Status Fields
    is_active: bool = Field(default=True, description="Account active status")
    last_login_at: Optional[datetime] = Field(
        default=None,
        description="Last login timestamp"
    )


class UserResponse(SQLModel):
    """
    Response schema for user data (excludes password_hash)
    Used for API responses to avoid exposing password hashes
    """
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    last_login_at: Optional[datetime] = None
