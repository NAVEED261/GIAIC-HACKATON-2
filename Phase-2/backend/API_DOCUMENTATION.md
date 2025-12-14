# API Documentation

## Overview

The Phase-2 API is a RESTful service for task management with user authentication and multi-user isolation.

- **Base URL:** `http://localhost:8000`
- **API Prefix:** `/api` (most endpoints), `/` (health checks)
- **Authentication:** JWT Bearer tokens
- **Documentation:** `/docs` (Swagger UI), `/redoc` (ReDoc)

---

## Authentication

### JWT Bearer Tokens

All protected endpoints require an `Authorization` header with a JWT token:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Obtaining Tokens

1. **Register (Sign Up):**
   ```http
   POST /api/auth/signup
   Content-Type: application/json

   {
     "email": "user@example.com",
     "name": "John Doe",
     "password": "securepassword123"
   }
   ```

2. **Login:**
   ```http
   POST /api/auth/login
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "securepassword123"
   }
   ```

   Response:
   ```json
   {
     "access_token": "eyJhbGc...",
     "refresh_token": "eyJhbGc...",
     "token_type": "bearer",
     "expires_in": 900
   }
   ```

### Token Expiry and Refresh

- **Access Token:** Expires in 15 minutes (900 seconds)
- **Refresh Token:** Expires in 7 days

Use refresh token to get new access token:
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}
```

---

## Endpoints

### Health Check Endpoints (No Authentication)

#### GET /health
Basic application health check.

**Request:**
```http
GET /health
```

**Response (200):**
```json
{
  "status": "healthy",
  "service": "task-management-api",
  "version": "2.0.0",
  "timestamp": "2025-01-03T16:45:00"
}
```

#### GET /health/db
Database connectivity check.

**Request:**
```http
GET /health/db
```

**Response (200):**
```json
{
  "status": "connected",
  "database": "ok",
  "service": "task-management-api",
  "version": "2.0.0",
  "timestamp": "2025-01-03T16:45:00",
  "response_time_ms": 5
}
```

---

### Authentication Endpoints

#### POST /api/auth/signup
Register a new user account.

**Request:**
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "name": "John Doe",
  "message": "User registered successfully"
}
```

**Error Responses:**
- `400`: Invalid email/password format, or password too weak
- `409`: Email already registered
- `500`: Server error

**Constraints:**
- Email must be valid email format and unique
- Password minimum 8 characters recommended
- Name required, 1-255 characters

---

#### POST /api/auth/login
Authenticate user and receive JWT tokens.

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Error Responses:**
- `401`: Invalid credentials
- `404`: User not found
- `500`: Server error

---

#### GET /api/auth/me
Get authenticated user's information.

**Request:**
```http
GET /api/auth/me
Authorization: Bearer eyJhbGc...
```

**Response (200):**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-01-01T10:00:00",
  "updated_at": "2025-01-01T10:00:00",
  "is_active": true,
  "last_login_at": "2025-01-03T15:00:00"
}
```

**Error Responses:**
- `401`: Not authenticated or token invalid
- `404`: User not found
- `500`: Server error

---

#### POST /api/auth/refresh
Refresh access token using refresh token.

**Request:**
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 900
}
```

**Error Responses:**
- `401`: Invalid or expired refresh token
- `500`: Server error

---

#### POST /api/auth/logout
Logout user and invalidate current token.

**Request:**
```http
POST /api/auth/logout
Authorization: Bearer eyJhbGc...
```

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses:**
- `401`: Not authenticated
- `500`: Server error

---

### Task Endpoints (Authenticated)

#### GET /api/tasks
List user's tasks (paginated).

**Request:**
```http
GET /api/tasks?skip=0&limit=10&status=Pending&sort_by=created_at&order=desc
Authorization: Bearer eyJhbGc...
```

**Query Parameters:**
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10, max=100): Items per page
- `status` (str, optional): Filter by status ("Pending", "Completed")
- `sort_by` (str, default="created_at"): Sort field
- `order` (str, default="desc"): Sort order (asc/desc)

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "Pending",
    "priority": "Medium",
    "created_at": "2025-01-03T10:00:00",
    "updated_at": "2025-01-03T10:00:00",
    "completed_at": null,
    "user_id": "uuid-here"
  },
  ...
]
```

**Error Responses:**
- `401`: Not authenticated
- `500`: Server error

---

#### POST /api/tasks
Create a new task.

**Request:**
```http
POST /api/tasks
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Pending",
  "priority": "Medium"
}
```

**Response (201):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Pending",
  "priority": "Medium",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T15:30:00",
  "completed_at": null,
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `400`: Invalid input (empty title, title too long)
- `401`: Not authenticated
- `500`: Server error

**Constraints:**
- `title`: Required, 1-200 characters
- `description`: Optional, up to 1000 characters
- `status`: Optional, defaults to "Pending"
- `priority`: Optional, defaults to "Medium"

---

#### GET /api/tasks/{id}
Get task details.

**Request:**
```http
GET /api/tasks/42
Authorization: Bearer eyJhbGc...
```

**Response (200):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Pending",
  "priority": "Medium",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T15:30:00",
  "completed_at": null,
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `401`: Not authenticated
- `403`: Access denied (task belongs to different user)
- `404`: Task not found
- `500`: Server error

---

#### PUT /api/tasks/{id}
Update an existing task.

**Request:**
```http
PUT /api/tasks/42
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "status": "In Progress",
  "priority": "High"
}
```

**Response (200):**
```json
{
  "id": 42,
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread",
  "status": "In Progress",
  "priority": "High",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T16:45:00",
  "completed_at": null,
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `400`: Invalid input
- `401`: Not authenticated
- `403`: Access denied (not task owner)
- `404`: Task not found
- `500`: Server error

**Note:** Partial updates supported - send only fields to update.

---

#### DELETE /api/tasks/{id}
Delete a task permanently.

**Request:**
```http
DELETE /api/tasks/42
Authorization: Bearer eyJhbGc...
```

**Response (204):**
No content returned.

**Error Responses:**
- `401`: Not authenticated
- `403`: Access denied (not task owner)
- `404`: Task not found
- `500`: Server error

---

#### PATCH /api/tasks/{id}/complete
Mark a task as completed.

**Request:**
```http
PATCH /api/tasks/42/complete
Authorization: Bearer eyJhbGc...
```

**Response (200):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Completed",
  "priority": "Medium",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T16:45:00",
  "completed_at": "2025-01-03T16:45:00",
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `401`: Not authenticated
- `403`: Access denied (not task owner)
- `404`: Task not found
- `409`: Task already completed
- `500`: Server error

---

## Error Handling

All error responses follow a consistent format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successfully retrieved resource |
| 201 | Created | Successfully created resource |
| 204 | No Content | Successfully deleted resource |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Access denied (not owner) |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Task already completed |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | Database down |

---

## Request/Response Formats

### JSON Format
All request bodies and responses use JSON format with `Content-Type: application/json`.

### Timestamps
All timestamps are in ISO 8601 format with UTC timezone:
```
2025-01-03T15:30:00
2025-01-03T16:45:00Z
```

### Pagination
List endpoints support pagination:
- `skip`: Offset (default 0)
- `limit`: Page size (default 10, max 100)

Example: Get page 2 with 10 items per page
```
GET /api/tasks?skip=10&limit=10
```

---

## Interactive Documentation

The API provides interactive documentation at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

You can test all endpoints directly in Swagger UI.

---

## Testing with cURL

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Create Task
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "Medium"
  }'
```

### List Tasks
```bash
curl -X GET "http://localhost:8000/api/tasks?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Multi-User Isolation

All task operations are automatically scoped to the authenticated user:

1. **List tasks:** Returns only user's tasks
2. **Create task:** Automatically assigned to user
3. **View task:** Only if user owns task (403 Forbidden otherwise)
4. **Update task:** Only if user owns task (403 Forbidden otherwise)
5. **Delete task:** Only if user owns task (403 Forbidden otherwise)

This is enforced at both the database and application level.

---

## Rate Limiting (Future)

Rate limiting will be added in Phase 2B. Once implemented:
- Default: 100 requests per minute
- Can be configured per endpoint
- Returns 429 Too Many Requests when exceeded

---

## Versioning Strategy

The API uses URL-based versioning:
- Current version: v1 (implied, no prefix in URLs)
- Future versions: `/api/v2/`, `/api/v3/`, etc.
- Backwards compatibility maintained in major versions

---

## CORS Configuration

CORS is enabled for development:
```
Allowed Origins: http://localhost:3000, http://localhost:8000
Allowed Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
Allowed Headers: *
```

Configure in `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## Example Workflow

### 1. Sign Up
```bash
POST /api/auth/signup
→ Create account, receive confirmation
```

### 2. Login
```bash
POST /api/auth/login
→ Receive access_token and refresh_token
```

### 3. Create Tasks
```bash
POST /api/tasks
→ With Authorization: Bearer {access_token}
→ Create multiple tasks
```

### 4. List Tasks
```bash
GET /api/tasks
→ View all personal tasks with pagination
```

### 5. Update Task
```bash
PUT /api/tasks/42
→ Modify task details
```

### 6. Mark Complete
```bash
PATCH /api/tasks/42/complete
→ Mark task as done
```

### 7. Refresh Token (When Access Expires)
```bash
POST /api/auth/refresh
→ Get new access token using refresh token
```

### 8. Logout
```bash
POST /api/auth/logout
→ Invalidate current session
```

---

## Support

For issues or questions:
1. Check `/docs` for interactive documentation
2. Review error messages for specific issues
3. Check application logs: `uvicorn main:app --log-level debug`
4. Refer to `MIGRATION_GUIDE.md` for database issues
