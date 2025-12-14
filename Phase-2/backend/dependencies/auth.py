"""
Authentication Dependencies

Provides reusable authentication functions:
- Password hashing and verification (bcrypt)
- JWT token generation and validation
- Current user extraction from token
- Token refresh logic

Used throughout routes to enforce authentication and authorization.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
import bcrypt

from db import get_db
from models.user import User

logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer scheme for extracting token from header
security = HTTPBearer(auto_error=False)

# JWT Configuration from environment
@lru_cache()
def get_jwt_config():
    """Get JWT configuration from environment variables."""
    return {
        "SECRET_KEY": os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-production"),
        "ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")),
        "REFRESH_TOKEN_EXPIRE_DAYS": int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
    }


# ============================================================================
# Password Hashing
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        str: Hashed password (can be stored in database)

    Security Notes:
        - bcrypt includes salt automatically
        - Cost factor (rounds) configurable in pwd_context
        - Output suitable for direct database storage
    """
    try:
        # Hash with bcrypt (uses salt internally)
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")
    except Exception as e:
        logger.error(f"Password hashing failed: {e}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain text password against bcrypt hash.

    Args:
        plain_password: Plain text password from user
        hashed_password: Stored hash from database

    Returns:
        bool: True if password matches, False otherwise

    Security Notes:
        - Uses constant-time comparison to prevent timing attacks
        - Returns False on error rather than raising exception
    """
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False


# ============================================================================
# JWT Token Management
# ============================================================================

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: User ID to encode in token
        expires_delta: Optional custom expiration time (default from config)

    Returns:
        str: Encoded JWT token

    Token Payload:
        {
            "user_id": "uuid-here",
            "exp": 1234567890,  # Expiration timestamp
            "iat": 1234567800,  # Issued at timestamp
            "type": "access"
        }

    Security Notes:
        - Access tokens are short-lived (default 15 minutes)
        - Token is signed with SECRET_KEY
        - Expiration enforced on validation
        - Use refresh token to get new access token
    """
    config = get_jwt_config()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config["ACCESS_TOKEN_EXPIRE_MINUTES"]
        )

    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access",
    }

    try:
        encoded_jwt = jwt.encode(
            payload,
            config["SECRET_KEY"],
            algorithm=config["ALGORITHM"],
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation failed: {e}")
        raise


def create_refresh_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token for a user.

    Args:
        user_id: User ID to encode in token
        expires_delta: Optional custom expiration time (default from config)

    Returns:
        str: Encoded JWT token

    Token Payload:
        {
            "user_id": "uuid-here",
            "exp": 1234567890,  # Expiration timestamp (7 days)
            "iat": 1234567800,  # Issued at timestamp
            "type": "refresh"
        }

    Security Notes:
        - Refresh tokens are long-lived (default 7 days)
        - Can be used to obtain new access tokens
        - Should be stored securely (httpOnly cookies preferred)
        - Revoked on logout (implementation-dependent)
    """
    config = get_jwt_config()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=config["REFRESH_TOKEN_EXPIRE_DAYS"]
        )

    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
    }

    try:
        encoded_jwt = jwt.encode(
            payload,
            config["SECRET_KEY"],
            algorithm=config["ALGORITHM"],
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Refresh token creation failed: {e}")
        raise


def decode_token(token: str, token_type: str = "access") -> dict:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token to decode
        token_type: Expected token type ("access" or "refresh")

    Returns:
        dict: Token payload if valid

    Raises:
        HTTPException 401: If token invalid, expired, or wrong type

    Validation Checks:
        - Signature is valid (not tampered with)
        - Expiration time hasn't passed
        - Token type matches expected type
        - user_id present in payload
    """
    config = get_jwt_config()

    try:
        payload = jwt.decode(
            token,
            config["SECRET_KEY"],
            algorithms=[config["ALGORITHM"]],
        )

        # Check token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}",
            )

        # Extract user_id
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user_id",
            )

        return payload

    except JWTError as e:
        logger.warning(f"JWT validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
    except Exception as e:
        logger.error(f"Token decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )


# ============================================================================
# FastAPI Dependencies
# ============================================================================

async def get_current_user(
    credentials: Optional[HTTPAuthCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI dependency to get authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException 401: If token missing, invalid, or user not found
        HTTPException 403: If user is inactive

    Usage in routes:
        @app.get("/api/tasks")
        async def list_tasks(current_user: User = Depends(get_current_user)):
            return current_user.tasks

    Token Extraction:
        - Gets token from "Authorization: Bearer <token>" header
        - Validates token signature and expiration
        - Looks up user in database
        - Returns User object for use in route
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # Decode and validate token
        payload = decode_token(token, token_type="access")
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # Look up user in database
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Optional authentication dependency (doesn't require token).

    Args:
        credentials: Optional HTTP Bearer token
        db: Database session

    Returns:
        Optional[User]: User if token valid, None otherwise

    Usage:
        When endpoint works with or without authentication.
        Returns None if no token, validated user if token present.
    """
    if not credentials:
        return None

    try:
        payload = decode_token(credentials.credentials, token_type="access")
        user_id = payload.get("user_id")

        if not user_id:
            return None

        user = db.query(User).filter(User.id == user_id).first()
        return user if user and user.is_active else None

    except Exception:
        return None
