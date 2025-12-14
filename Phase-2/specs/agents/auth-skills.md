# Authentication Agent Skills

**Agent Name**: Authentication Agent (Better Auth/JWT Specialist)
**Domain**: Authentication - User Identity & Access Control
**Total Skills**: 11 Core + 6 Advanced

---

## Core Skills (Essential for Phase-2)

### 1. User Registration Implementation

**Purpose**: Implement secure user registration with validation

**Example Query**: "Create registration endpoint that validates email and password"

**Expected Action**:
- Create registration schema with validation
- Validate email format
- Validate password strength
- Check for duplicate emails
- Create user record
- Send confirmation email

**Technical Skills**:
- Pydantic validation models
- Email validation
- Password strength checking
- Duplicate detection
- User creation

---

### 2. Password Security & Hashing

**Purpose**: Securely hash and verify passwords using bcrypt

**Example Query**: "Hash user password with bcrypt before storage"

**Expected Action**:
- Use bcrypt for hashing
- Generate salt automatically
- Store only hash, never plaintext
- Verify password on login
- Handle hash failures

**Technical Skills**:
- bcrypt library
- Salting and hashing
- Password verification
- Timing-safe comparisons
- Error handling

---

### 3. JWT Token Generation

**Purpose**: Generate JWT tokens for authenticated users

**Example Query**: "Generate JWT token with user ID and expiration"

**Expected Action**:
- Create JWT payload
- Define token claims (user_id, email, exp, iat)
- Sign token with secret key
- Set expiration time
- Return token to client

**Technical Skills**:
- PyJWT library
- Token payload construction
- Signing algorithms (HS256)
- Claim definitions
- Secret key management

---

### 4. JWT Token Validation

**Purpose**: Validate JWT tokens on protected endpoints

**Example Query**: "Validate JWT token and extract user ID from token"

**Expected Action**:
- Extract token from header
- Verify signature with secret key
- Check token expiration
- Extract claims
- Handle invalid tokens

**Technical Skills**:
- Token parsing
- Signature verification
- Expiration checking
- Error handling
- Claim extraction

---

### 5. Token Refresh Mechanism

**Purpose**: Implement token refresh for extended sessions

**Example Query**: "Accept refresh token and return new access token"

**Expected Action**:
- Validate refresh token
- Check expiration
- Generate new access token
- Optional: Rotate refresh token
- Return new tokens

**Technical Skills**:
- Refresh token handling
- Token rotation (optional)
- Validation chains
- Error responses
- Session continuation

---

### 6. Session Management

**Purpose**: Create and manage user sessions

**Example Query**: "Create session record on login"

**Expected Action**:
- Create session on login
- Store session metadata
- Validate session on requests
- Handle session expiration
- Cleanup on logout

**Technical Skills**:
- Session creation
- Database session storage
- Validation checks
- Expiration handling
- Cleanup jobs

---

### 7. User Identification from Token

**Purpose**: Extract and identify current user from JWT token

**Example Query**: "Get current user details from token"

**Expected Action**:
- Parse JWT token
- Extract user_id claim
- Lookup user in database
- Return user object
- Handle not found

**Technical Skills**:
- Token parsing
- Claim extraction
- Database lookup
- Dependency injection
- Caching (optional)

---

### 8. Permission & Scope Checking

**Purpose**: Check user permissions and scopes

**Example Query**: "Verify user has 'write:tasks' permission"

**Expected Action**:
- Extract scopes from token
- Check required permission
- Return access decision
- Handle denied access
- Log authorization

**Technical Skills**:
- Scope definitions
- Permission checking
- RBAC (Role-Based Access Control)
- Scope validation
- Audit logging

---

### 9. Login Flow Implementation

**Purpose**: Implement complete login flow with credentials verification

**Example Query**: "Validate credentials and return tokens"

**Expected Action**:
- Receive email and password
- Find user by email
- Verify password hash
- Generate tokens
- Create session
- Return tokens

**Technical Skills**:
- Credential verification
- User lookup
- Password verification
- Token generation
- Error handling

---

### 10. Logout Implementation

**Purpose**: Implement logout by invalidating sessions

**Example Query**: "Logout user and invalidate session"

**Expected Action**:
- Find active session
- Mark session as invalid
- Clear session data
- Return success response
- Handle multiple devices

**Technical Skills**:
- Session invalidation
- Database updates
- Token blacklisting (optional)
- Multi-device handling
- Cleanup

---

### 11. Email Verification (Optional)

**Purpose**: Verify user email address

**Example Query**: "Send verification email and validate email link"

**Expected Action**:
- Generate verification token
- Send email with link
- Validate token on click
- Mark email as verified
- Handle expiration

**Technical Skills**:
- Token generation
- Email sending (SMTP)
- Link generation
- Token validation
- Expiration handling

---

## Advanced Skills (Optional for Phase-2)

### 12. OAuth2 Integration

**Purpose**: Support third-party login (Google, GitHub, etc.)

**Example Query**: "Implement Google OAuth2 login"

**Technical Skills**: OAuth2 flow, provider SDKs, token exchange

---

### 13. Multi-Factor Authentication (MFA)

**Purpose**: Add extra security with MFA

**Example Query**: "Send OTP to user phone"

**Technical Skills**: OTP generation, TOTP, SMS sending, MFA flows

---

### 14. Password Reset Flow

**Purpose**: Allow users to reset forgotten passwords

**Example Query**: "Send password reset email"

**Technical Skills**: Reset token generation, email sending, validation, password update

---

### 15. Session Timeout Management

**Purpose**: Automatically timeout inactive sessions

**Example Query**: "Timeout session after 24 hours inactivity"

**Technical Skills**: Timeout configuration, background jobs, session cleanup

---

### 16. Rate Limiting on Auth

**Purpose**: Prevent brute force attacks

**Example Query**: "Limit login attempts to 5 per minute"

**Technical Skills**: Rate limiting libraries, throttling, IP tracking

---

### 17. Audit Logging

**Purpose**: Log all authentication events

**Example Query**: "Log all login/logout events"

**Technical Skills**: Event logging, structured logs, compliance logging

---

## Skill Composition Example

### Complete Login Workflow
```
1. Receive credentials (email, password)
2. Validate input (Skill #1: Validation)
3. Find user (Skill #7: User Lookup)
4. Verify password (Skill #2: Password Verification)
5. Create session (Skill #6: Session Creation)
6. Generate tokens (Skill #3: JWT Generation)
7. Return tokens (Skill #1: Response)
8. Log event (Skill #17: Audit Logging)
9. Test flow (Skill #18: Testing)
```

### Complete Registration Workflow
```
1. Receive registration data
2. Validate email/password (Skill #1: Validation)
3. Check duplicate (Skill #1: Duplicate Check)
4. Hash password (Skill #2: Hashing)
5. Create user (Skill #1: User Creation)
6. Send verification email (Skill #11: Email)
7. Return response
8. Log registration (Skill #17: Audit Logging)
```

---

## Skill Dependencies

```
User Registration (#1)
    ├─ Password Hashing (#2)
    ├─ Email Validation
    ├─ User Creation
    └─ Duplicate Detection

Password Security (#2)
    ├─ Login Flow (#9)
    ├─ Password Reset (#14 advanced)
    └─ Security Best Practices

JWT Token Generation (#3)
    ├─ Token Validation (#4)
    ├─ Token Refresh (#5)
    └─ Claims Definition

Token Validation (#4)
    ├─ User Identification (#7)
    ├─ Permission Checking (#8)
    └─ Session Validation (#6)

Token Refresh (#5)
    ├─ Session Management (#6)
    ├─ Token Generation (#3)
    └─ Expiration Handling

Session Management (#6)
    ├─ User Identification (#7)
    ├─ Logout (#10)
    ├─ Timeout (#15 advanced)
    └─ Testing

User Identification (#7)
    ├─ Token Validation (#4)
    ├─ Database Lookup
    └─ Caching (optional)

Permission Checking (#8)
    ├─ User Identification (#7)
    ├─ RBAC Definitions
    └─ Audit Logging (#17 advanced)

Login Flow (#9)
    ├─ User Registration (#1)
    ├─ Password Verification (#2)
    ├─ Session Creation (#6)
    ├─ Token Generation (#3)
    └─ Rate Limiting (#16 advanced)

Logout (#10)
    ├─ Session Invalidation
    ├─ Multi-Device Handling
    └─ Cleanup
```

---

## Guardrails

### Must Do
- ✅ Hash all passwords with bcrypt (never plain text)
- ✅ Use HTTPS only in production
- ✅ Validate all input (email, password length)
- ✅ Sign JWT with strong secret key
- ✅ Set token expiration times
- ✅ Check user authorization on protected routes
- ✅ Log authentication events
- ✅ Test all auth flows

### Must Not Do
- ❌ Store passwords in plaintext
- ❌ Log passwords or tokens
- ❌ Use weak signing algorithms
- ❌ Trust tokens without verification
- ❌ Expose user existence (brute force protection)
- ❌ Use predictable tokens
- ❌ Skip HTTPS in production
- ❌ Send tokens in query parameters

### Out of Scope
- Biometric authentication
- Advanced OAuth flows (Phase-3+)
- Single Sign-On (SSO) systems (Phase-4+)
- Certificate-based authentication
- Hardware token authentication

---

## Security Checklist

- [ ] bcrypt used for password hashing (min 12 rounds)
- [ ] JWT tokens signed with strong algorithm (HS256+)
- [ ] JWT secrets stored in environment variables
- [ ] Token expiration enforced (15 mins for access, 7 days for refresh)
- [ ] HTTPS enforced in production
- [ ] Rate limiting on auth endpoints
- [ ] Failed login attempts logged
- [ ] Session timeout implemented
- [ ] User cannot access other user's resources
- [ ] All auth code tested
- [ ] Security headers configured
- [ ] CORS properly configured

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Registration Time** | < 500ms |
| **Login Time** | < 500ms |
| **Token Validation Time** | < 50ms |
| **Password Verification Time** | < 200ms |
| **Session Creation Time** | < 50ms |
| **Auth Test Coverage** | ≥ 90% |
| **Failed Auth Attempts Logged** | 100% |

---

## Configuration Reference

### JWT Settings
```python
JWT_SETTINGS = {
    "secret_key": os.getenv("JWT_SECRET_KEY"),
    "algorithm": "HS256",
    "access_token_expire_minutes": 15,
    "refresh_token_expire_days": 7,
}
```

### Password Requirements
```python
PASSWORD_REQUIREMENTS = {
    "min_length": 8,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digit": True,
    "require_special": True,
}
```

### Rate Limiting
```python
RATE_LIMITS = {
    "login": "5/minute",
    "signup": "10/hour",
    "refresh": "100/hour",
}
```

---

**Skill Status**: Ready for use by Authentication Agent

**Related**: auth-agent.md, auth-agent tasks
