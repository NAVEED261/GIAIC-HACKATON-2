# Authentication Agent Specification

**Agent Name**: Authentication Agent (Better Auth/JWT Specialist)
**Domain**: Authentication - User Identity & Access Control
**Technology**: Better Auth, PyJWT, Pydantic, bcrypt
**Responsibility**: Implement secure authentication, authorization, and session management
**Created**: 2025-12-14

---

## Agent Overview

The Authentication Agent is responsible for implementing secure user authentication, JWT token management, authorization, and session handling for the Phase-2 full-stack application.

### Primary Responsibilities

1. **User Authentication**
   - User registration with validation
   - User login with credentials verification
   - Password hashing and verification
   - Email validation
   - Account activation/confirmation

2. **JWT Token Management**
   - JWT token generation
   - Token refresh mechanism
   - Token expiration handling
   - Token validation and verification
   - Token revocation

3. **Session Management**
   - Session creation on login
   - Session validation on requests
   - Session expiration
   - Session cleanup
   - Multi-device session handling

4. **Authorization**
   - Role-based access control (RBAC)
   - Permission checking
   - Resource-level authorization
   - Scope validation
   - Authorization error handling

5. **Security**
   - Password security best practices
   - Salt and hash implementation
   - Token signing with secrets
   - HTTPS enforcement
   - CORS policy enforcement
   - Rate limiting on auth endpoints

6. **Testing**
   - Registration flow tests
   - Login flow tests
   - Token validation tests
   - Authorization tests
   - Security tests
   - Edge case tests

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Auth Framework** | Better Auth | Authentication library |
| **JWT** | PyJWT | JWT token handling |
| **Hashing** | bcrypt | Password hashing |
| **Validation** | Pydantic | Data validation |
| **Sessions** | Database/Redis | Session storage |
| **Testing** | pytest | Auth tests |

---

## Deliverables

### Authentication Routes (routes/auth.py)
- POST /api/auth/signup - User registration
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout
- POST /api/auth/refresh - Token refresh
- GET /api/auth/me - Current user info
- POST /api/auth/verify-email - Email verification

### Models (models/auth.py)
- User authentication model
- JWT payload schema
- Login credentials schema
- Registration schema
- Token response schema

### Utils (utils/security.py)
- Password hashing functions
- Password verification functions
- JWT token creation
- JWT token verification
- Token payload extraction

### Middleware (middleware/auth.py)
- JWT validation middleware
- Current user extraction
- Permission checking middleware
- Rate limiting middleware
- Error handling middleware

### Services (services/auth_service.py)
- Authentication service
- Token management service
- Session service
- Authorization service

### Testing (tests/auth/)
- `test_registration.py` - Registration tests
- `test_login.py` - Login tests
- `test_tokens.py` - Token tests
- `test_authorization.py` - Authorization tests
- `test_security.py` - Security tests
- `conftest.py` - Auth fixtures

---

## Authentication Flow

### Registration Flow
```
User Input (email, password, name)
    ↓
Validate Input (email format, password strength)
    ↓
Check if User Exists (email uniqueness)
    ↓
Hash Password (bcrypt with salt)
    ↓
Create User Record
    ↓
Send Verification Email
    ↓
Return Success + Instructions
```

### Login Flow
```
User Input (email, password)
    ↓
Validate Credentials (email exists, password matches)
    ↓
Generate JWT Token
    ↓
Create Session Record
    ↓
Return Token + User Info
```

### Token Refresh Flow
```
Receive Refresh Token
    ↓
Validate Refresh Token
    ↓
Check Token Expiration
    ↓
Generate New Access Token
    ↓
Return New Token
```

### Protected Request Flow
```
Receive Request with Token
    ↓
Extract Token from Header
    ↓
Validate Token Signature
    ↓
Check Token Expiration
    ↓
Extract User ID from Token
    ↓
Allow Request / Reject
```

---

## Data Models

### User Registration Schema
```python
class UserRegisterRequest(BaseModel):
    email: str  # Valid email format
    password: str  # Min 8 chars, mix of upper/lower/number/special
    name: str  # 1-100 chars
    password_confirm: str  # Must match password

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be 8+ characters')
        return v
```

### User Login Schema
```python
class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    user: UserResponse
```

### JWT Payload Schema
```python
class JWTPayload(BaseModel):
    user_id: str
    email: str
    iat: int  # Issued at
    exp: int  # Expiration
    scopes: List[str] = []  # User permissions
```

### User Response Schema
```python
class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

---

## Key Features to Implement

### 1. User Registration
- Email validation and normalization
- Password strength validation (min 8 chars, mix of character types)
- Password confirmation matching
- User record creation
- Email verification flow
- Duplicate email prevention

### 2. Password Security
- bcrypt hashing with salt
- Password strength requirements
- Password history (prevent reuse)
- Password reset flow
- Secure password storage
- Timeout on failed attempts

### 3. JWT Token Management
- Access token generation (short-lived, 15 mins)
- Refresh token generation (long-lived, 7 days)
- Token signing with secret key
- Token claims (user_id, email, scopes, exp, iat)
- Token expiration validation
- Token signature verification

### 4. Session Management
- Session creation on login
- Session validation on protected routes
- Session expiration (24 hours or user logout)
- Logout invalidates session
- Multiple sessions per user (optional)
- Session cleanup jobs

### 5. Authorization & Permissions
- User identification from token
- Role-based access control (Admin, User)
- Permission scopes (read:tasks, write:tasks)
- Resource-level authorization
- 403 Forbidden on insufficient permissions
- Audit logging of authorization failures

### 6. Security Best Practices
- HTTPS enforcement
- CORS policy validation
- CSRF token handling
- Rate limiting on auth endpoints (5 attempts/min)
- Password attempt throttling
- Secure token storage on client
- httpOnly cookie options

### 7. Error Handling
- 400 Bad Request - Invalid input
- 401 Unauthorized - Invalid credentials
- 403 Forbidden - Insufficient permissions
- 409 Conflict - User already exists
- 422 Unprocessable Entity - Validation errors
- Clear error messages (no password hints)

### 8. Logging & Monitoring
- Failed login attempts
- Successful logins
- Token refresh operations
- Authorization failures
- Password change operations
- Security events

---

## API Endpoints

### Registration
```
POST /api/auth/signup
Request:
{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "name": "John Doe"
}
Response:
{
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe",
    "message": "Check your email for verification"
}
```

### Login
```
POST /api/auth/login
Request:
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
Response:
{
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "Bearer",
    "user": {
        "id": "user_123",
        "email": "user@example.com",
        "name": "John Doe"
    }
}
```

### Logout
```
POST /api/auth/logout
Headers: Authorization: Bearer {token}
Response:
{
    "message": "Logged out successfully"
}
```

### Token Refresh
```
POST /api/auth/refresh
Request:
{
    "refresh_token": "eyJhbGc..."
}
Response:
{
    "access_token": "eyJhbGc...",
    "token_type": "Bearer"
}
```

### Current User
```
GET /api/auth/me
Headers: Authorization: Bearer {token}
Response:
{
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe",
    "is_active": true,
    "created_at": "2025-12-14T10:00:00Z"
}
```

---

## Testing Requirements

### Unit Tests
- Password hashing and verification
- Token generation and validation
- Payload extraction
- Permission checking
- Email validation

### Integration Tests
- Complete registration flow
- Complete login flow
- Token refresh flow
- Protected route access
- Logout flow
- Session creation and cleanup
- Authorization checks

### Security Tests
- Weak password rejection
- Duplicate email prevention
- Expired token rejection
- Invalid token signature rejection
- Missing token handling
- Rate limiting on login attempts
- Password history enforcement

### Edge Cases
- Missing required fields
- Invalid email format
- Password mismatch
- User not found
- Expired refresh token
- Revoked token
- Concurrent login attempts

---

## Configuration

### Environment Variables
```
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_MIN_LENGTH=8
MAX_LOGIN_ATTEMPTS=5
LOGIN_ATTEMPT_TIMEOUT=300
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### JWT Configuration
```python
JWT_SETTINGS = {
    "secret_key": os.getenv("JWT_SECRET_KEY"),
    "algorithm": "HS256",
    "access_token_expire_minutes": 15,
    "refresh_token_expire_days": 7,
}
```

---

## Performance Targets

| Metric | Target |
|--------|--------|
| **Registration Time** | < 500ms |
| **Login Time** | < 500ms |
| **Token Validation** | < 50ms |
| **Password Verification** | < 200ms (bcrypt) |
| **Token Refresh** | < 100ms |
| **Authorization Check** | < 50ms |
| **Concurrent Auth Users** | 1,000+ |

---

## Acceptance Criteria

- [ ] User registration implemented with validation
- [ ] Password hashing with bcrypt
- [ ] JWT token generation and validation
- [ ] Token refresh mechanism working
- [ ] Session management implemented
- [ ] Authorization checks enforced
- [ ] All auth endpoints working
- [ ] Rate limiting on auth endpoints
- [ ] Email verification flow working
- [ ] All tests passing (≥80% coverage)
- [ ] No passwords in logs
- [ ] Security best practices followed
- [ ] Error messages user-friendly (no leaks)
- [ ] HTTPS enforced in production

---

## Related Specifications

- `@specs/features/authentication.md` - Auth requirements
- `@specs/agents/backend-agent.md` - Backend integration
- `@specs/agents/frontend-agent.md` - Frontend integration
- `@specs/database/schema.md` - User schema

---

**Agent Status**: 🔄 Ready for Implementation

**Next Step**: Follow `auth-skills.md` for detailed capabilities
