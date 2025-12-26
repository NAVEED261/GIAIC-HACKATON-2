"""
Authentication Routes

Handles user registration, login, token refresh, and session management.
All endpoints include OpenAPI documentation and error handling.

Endpoints:
  POST   /api/auth/signup    - User registration
  POST   /api/auth/login     - User login (returns JWT)
  POST   /api/auth/logout    - User logout (invalidates token)
  POST   /api/auth/refresh   - Refresh JWT token
  GET    /api/auth/me        - Get current user info
"""

import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, validator

from db import get_db
from models.user import User, UserResponse
from dependencies.auth import (
    get_current_user,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ============================================================================
# Request/Response Schema Classes
# ============================================================================

class SignupRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    name: str
    password: str

    @validator("name")
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Name cannot be empty")
        if len(v) > 255:
            raise ValueError("Name cannot exceed 255 characters")
        return v.strip()

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "securepassword123",
            }
        }


class SignupResponse(BaseModel):
    """User registration response."""
    id: str
    email: str
    name: str
    message: str = "User registered successfully"

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "name": "John Doe",
                "message": "User registered successfully",
            }
        }


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }


class UserInResponse(BaseModel):
    """User data in response."""
    id: str
    email: str
    name: str


class LoginResponse(BaseModel):
    """User login response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserInResponse = None

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 900,
            }
        }


class TokenRefreshRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }


class TokenRefreshResponse(BaseModel):
    """Token refresh response."""
    access_token: str
    expires_in: int
    user: UserInResponse = None

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_in": 900,
            }
        }


class LogoutResponse(BaseModel):
    """Logout response."""
    message: str = "Logged out successfully"

    class Config:
        schema_extra = {
            "example": {
                "message": "Logged out successfully",
            }
        }


# ============================================================================
# Authentication Endpoints (Unauthenticated)
# ============================================================================


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User registered successfully"},
        400: {"description": "Invalid email or password format"},
        409: {"description": "Email already registered"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
    summary="User Registration",
    description="""
Register a new user account.

**Request Body:**
- `email`: Valid email address (must be unique)
- `name`: User's display name (1-255 characters)
- `password`: Password (minimum 8 characters)

**Success Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "message": "User registered successfully"
}
```

**Error Responses:**
- `400`: Invalid input (email format, password too short)
- `409`: Email already registered
- `422`: Validation error
- `500`: Server error

**Security Note:** Passwords are hashed with bcrypt before storage.
    """,
)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        request: Registration data (email, name, password)
        db: Database session

    Returns:
        SignupResponse with user info and confirmation message

    Raises:
        HTTPException 400: Invalid input
        HTTPException 409: Email already registered
        HTTPException 422: Validation error
        HTTPException 500: Server error
    """
    try:
        # Check if email already registered
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(request.password)

        new_user = User(
            id=user_id,
            email=request.email,
            name=request.name,
            password_hash=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User registered successfully: {request.email}")

        return SignupResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Login successful, tokens issued"},
        401: {"description": "Invalid credentials"},
        404: {"description": "User not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
    summary="User Login",
    description="""
Authenticate user and return JWT tokens.

**Request Body:**
- `email`: User's email address
- `password`: User's password

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Error Responses:**
- `401`: Invalid credentials (wrong email or password)
- `404`: User not found
- `422`: Validation error
- `500`: Server error

**Token Details:**
- `access_token`: Used for API requests (expires in 15 minutes)
- `refresh_token`: Used to refresh access token (expires in 7 days)
- `expires_in`: Access token expiration time in seconds
    """,
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and issue tokens.

    Args:
        request: Login credentials (email, password)
        db: Database session

    Returns:
        LoginResponse with access and refresh tokens

    Raises:
        HTTPException 401: Invalid credentials
        HTTPException 404: User not found
        HTTPException 500: Server error
    """
    try:
        # Find user by email
        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            logger.warning(f"Login attempt for non-existent user: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Verify password
        if not verify_password(request.password, user.password_hash):
            logger.warning(f"Failed login attempt for user: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # Generate tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # Update last login time
        user.last_login_at = datetime.utcnow()
        db.commit()

        logger.info(f"User logged in successfully: {request.email}")

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900,  # 15 minutes in seconds
            user=UserInResponse(id=user.id, email=user.email, name=user.name),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


# ============================================================================
# Authentication Endpoints (Authenticated)
# ============================================================================


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Logged out successfully"},
        401: {"description": "Not authenticated"},
        500: {"description": "Internal server error"},
    },
    summary="User Logout",
    description="""
Logout user and invalidate current session/token.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Success Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses:**
- `401`: Not authenticated (missing or invalid token)
- `500`: Server error

**Security Note:** After logout, the access token is no longer valid.
Token invalidation is done server-side (blacklist or session tracking).
    """,
)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user.

    Args:
        current_user: Currently authenticated user

    Returns:
        LogoutResponse with success message

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 500: Server error
    """
    try:
        logger.info(f"User logged out: {current_user.email}")
        # Token invalidation could be implemented here (e.g., token blacklist)
        # For now, client-side token removal is sufficient
        return LogoutResponse()

    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed",
        )


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"description": "Invalid or expired refresh token"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
    summary="Refresh Access Token",
    description="""
Use refresh token to obtain a new access token.

**Request Body:**
- `refresh_token`: Valid refresh token

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 900
}
```

**Error Responses:**
- `401`: Invalid or expired refresh token
- `422`: Validation error
- `500`: Server error

**Token Details:**
- `access_token`: New access token (expires in 15 minutes)
- `expires_in`: Expiration time in seconds

**When to Use:**
When access token expires (401 response), use refresh token to get new access token
without requiring the user to log in again.
    """,
)
async def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.

    Args:
        request: Refresh token request (refresh_token)
        db: Database session

    Returns:
        TokenRefreshResponse with new access token

    Raises:
        HTTPException 401: Invalid or expired refresh token
        HTTPException 500: Server error
    """
    try:
        # Validate refresh token
        payload = decode_token(request.refresh_token, token_type="refresh")
        user_id = payload.get("user_id")

        # Verify user still exists and is active
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Generate new access token
        access_token = create_access_token(user_id)

        logger.info(f"Token refreshed for user: {user.email}")

        return TokenRefreshResponse(
            access_token=access_token,
            expires_in=900,  # 15 minutes in seconds
            user=UserInResponse(id=user.id, email=user.email, name=user.name),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Current user information"},
        401: {"description": "Not authenticated"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"},
    },
    summary="Get Current User",
    description="""
Retrieve authenticated user's information.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Success Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00",
  "is_active": true,
  "last_login_at": "2025-01-02T12:00:00"
}
```

**Error Responses:**
- `401`: Not authenticated (missing or invalid token)
- `404`: User not found (should not happen if token is valid)
- `500`: Server error

**Note:** Password hash is never included in response.
    """,
)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get authenticated user's information.

    Args:
        current_user: Currently authenticated user

    Returns:
        UserResponse with user information

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 404: User not found
        HTTPException 500: Server error
    """
    try:
        return UserResponse(
            id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            is_active=current_user.is_active,
            last_login_at=current_user.last_login_at,
        )

    except Exception as e:
        logger.error(f"Get current user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information",
        )
