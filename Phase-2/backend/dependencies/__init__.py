"""
Dependencies Package

Provides reusable FastAPI dependencies and helper functions.

Modules:
  auth - Authentication, password hashing, JWT token management
"""

from .auth import (
    get_current_user,
    get_current_user_optional,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

__all__ = [
    "get_current_user",
    "get_current_user_optional",
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
]
