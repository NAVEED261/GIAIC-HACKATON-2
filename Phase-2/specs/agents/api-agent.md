# API Agent Specification

**Agent Name**: API Agent (REST API Design Specialist)
**Domain**: API - REST Endpoint Architecture & Contracts
**Technology**: FastAPI, OpenAPI/Swagger, Pydantic, REST Principles
**Responsibility**: Design and document RESTful API contracts and standards
**Created**: 2025-12-14

---

## Agent Overview

The API Agent is responsible for designing consistent RESTful API contracts, endpoint specifications, request/response formats, error handling standards, and API documentation for the Phase-2 full-stack application.

### Primary Responsibilities

1. **API Design & Architecture**
   - Design RESTful endpoints following REST principles
   - Define resource-based URL structure
   - HTTP method mapping (GET, POST, PUT, PATCH, DELETE)
   - Versioning strategy
   - API consistency and conventions

2. **Request/Response Contracts**
   - Request body specifications
   - Response body specifications
   - HTTP status code definitions
   - Error response formats
   - Pagination standards
   - Filter and sort parameters

3. **Documentation**
   - OpenAPI/Swagger documentation
   - Endpoint descriptions and examples
   - Request/response examples
   - Error scenarios
   - Authentication requirements
   - Rate limiting documentation

4. **Standardization**
   - Naming conventions
   - Field naming standards (camelCase, snake_case)
   - Date/time formats (ISO 8601)
   - Pagination format
   - Error response format
   - Success response format

5. **API Versioning**
   - Version strategy (URL path, header)
   - Backward compatibility
   - Deprecation policy
   - Migration guides
   - Breaking change handling

6. **Testing & Validation**
   - API contract tests
   - Response validation tests
   - Error handling tests
   - Performance tests
   - Integration tests

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | FastAPI | REST API framework |
| **Documentation** | OpenAPI/Swagger | API documentation |
| **Validation** | Pydantic | Request/response validation |
| **Testing** | pytest | API contract tests |
| **Mocking** | pytest-mock | API mocking |

---

## Deliverables

### API Specifications (specs/)
- `specs/api/rest-endpoints.md` - Complete endpoint specifications
- `specs/api/request-response.md` - Request/response formats
- `specs/api/error-handling.md` - Error response standards
- `specs/api/pagination.md` - Pagination standards
- `specs/api/authentication.md` - Auth requirements
- `specs/api/rate-limiting.md` - Rate limit policies

### OpenAPI Schema
- `openapi/openapi.json` - OpenAPI 3.0.0 specification
- `openapi/paths/tasks.yaml` - Task endpoints
- `openapi/paths/auth.yaml` - Auth endpoints
- `openapi/paths/health.yaml` - Health endpoints
- `openapi/schemas/task.yaml` - Task schema
- `openapi/schemas/user.yaml` - User schema
- `openapi/schemas/error.yaml` - Error schema

### API Routes Documentation
- Task endpoints documentation
- Auth endpoints documentation
- Health endpoints documentation
- User endpoints documentation

### Testing (tests/api/)
- `test_endpoints.py` - Endpoint contract tests
- `test_responses.py` - Response validation tests
- `test_errors.py` - Error handling tests
- `test_pagination.py` - Pagination tests
- `conftest.py` - API test fixtures

---

## REST API Principles

### Resource-Based URLs
```
/api/tasks              - Task collection
/api/tasks/{id}         - Specific task
/api/tasks/{id}/items   - Nested resources
/api/users              - User collection
/api/auth               - Authentication operations
```

### HTTP Methods
```
GET     - Retrieve resource(s)
POST    - Create new resource
PUT     - Replace entire resource
PATCH   - Partial update
DELETE  - Remove resource
HEAD    - Like GET, no response body
OPTIONS - Available methods
```

### HTTP Status Codes
```
2xx Success
  200 OK
  201 Created
  202 Accepted
  204 No Content

3xx Redirection
  301 Moved Permanently
  302 Found
  304 Not Modified

4xx Client Error
  400 Bad Request
  401 Unauthorized
  403 Forbidden
  404 Not Found
  409 Conflict
  422 Unprocessable Entity

5xx Server Error
  500 Internal Server Error
  502 Bad Gateway
  503 Service Unavailable
```

---

## API Endpoint Specifications

### Task Endpoints

#### List Tasks
```
GET /api/tasks
Query Parameters:
  - status: string (optional) - Filter by status (Pending, Completed)
  - page: integer (optional) - Page number, default 1
  - limit: integer (optional) - Items per page, default 50, max 100
  - sort: string (optional) - Sort field (created_at, title, status)
  - order: string (optional) - asc or desc

Response (200 OK):
{
    "data": [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "Pending",
            "created_at": "2025-12-14T10:00:00Z",
            "updated_at": "2025-12-14T10:00:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 50,
        "total": 150,
        "pages": 3
    }
}
```

#### Create Task
```
POST /api/tasks
Headers: Authorization: Bearer {token}
Request Body:
{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
}

Response (201 Created):
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "Pending",
    "created_at": "2025-12-14T10:00:00Z",
    "updated_at": "2025-12-14T10:00:00Z"
}
```

#### Get Task
```
GET /api/tasks/{id}
Headers: Authorization: Bearer {token}

Response (200 OK):
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "Pending",
    "created_at": "2025-12-14T10:00:00Z",
    "updated_at": "2025-12-14T10:00:00Z"
}

Response (404 Not Found):
{
    "error_code": "NOT_FOUND",
    "message": "Task not found"
}
```

#### Update Task
```
PUT /api/tasks/{id}
Headers: Authorization: Bearer {token}
Request Body:
{
    "title": "Update task",
    "description": "New description",
    "status": "Pending"
}

Response (200 OK):
{
    "id": 1,
    "title": "Update task",
    "description": "New description",
    "status": "Pending",
    "created_at": "2025-12-14T10:00:00Z",
    "updated_at": "2025-12-14T10:30:00Z"
}
```

#### Delete Task
```
DELETE /api/tasks/{id}
Headers: Authorization: Bearer {token}

Response (204 No Content)
```

#### Mark Task Complete
```
PATCH /api/tasks/{id}/complete
Headers: Authorization: Bearer {token}

Response (200 OK):
{
    "id": 1,
    "title": "Buy groceries",
    "status": "Completed",
    "completed_at": "2025-12-14T10:30:00Z",
    "updated_at": "2025-12-14T10:30:00Z"
}
```

### Authentication Endpoints

#### Signup
```
POST /api/auth/signup
Request Body:
{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "name": "John Doe"
}

Response (201 Created):
{
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe"
}
```

#### Login
```
POST /api/auth/login
Request Body:
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}

Response (200 OK):
{
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "Bearer"
}
```

#### Logout
```
POST /api/auth/logout
Headers: Authorization: Bearer {token}

Response (200 OK):
{
    "message": "Logged out successfully"
}
```

#### Token Refresh
```
POST /api/auth/refresh
Request Body:
{
    "refresh_token": "eyJhbGc..."
}

Response (200 OK):
{
    "access_token": "eyJhbGc...",
    "token_type": "Bearer"
}
```

#### Current User
```
GET /api/auth/me
Headers: Authorization: Bearer {token}

Response (200 OK):
{
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe",
    "is_active": true,
    "created_at": "2025-12-14T10:00:00Z"
}
```

### Health Endpoints

#### Health Check
```
GET /health

Response (200 OK):
{
    "status": "healthy",
    "timestamp": "2025-12-14T10:00:00Z"
}
```

#### Database Health
```
GET /health/db

Response (200 OK):
{
    "status": "connected",
    "response_time": 15,
    "timestamp": "2025-12-14T10:00:00Z"
}
```

---

## Error Response Format

### Standard Error Response
```json
{
    "error_code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": {
        "field": "title",
        "issue": "Title cannot be empty",
        "received": ""
    },
    "timestamp": "2025-12-14T10:00:00Z",
    "request_id": "req_abc123"
}
```

### Error Codes
- `VALIDATION_ERROR` - 422 Unprocessable Entity
- `UNAUTHORIZED` - 401 Unauthorized (invalid/missing token)
- `FORBIDDEN` - 403 Forbidden (insufficient permissions)
- `NOT_FOUND` - 404 Not Found (resource not found)
- `CONFLICT` - 409 Conflict (resource already exists)
- `INTERNAL_ERROR` - 500 Internal Server Error
- `SERVICE_UNAVAILABLE` - 503 Service Unavailable
- `RATE_LIMITED` - 429 Too Many Requests

---

## Pagination Standard

### Request Format
```
GET /api/tasks?page=2&limit=50&sort=created_at&order=desc
```

### Response Format
```json
{
    "data": [...],
    "pagination": {
        "page": 2,
        "limit": 50,
        "total": 250,
        "pages": 5,
        "has_next": true,
        "has_previous": true
    }
}
```

### Defaults & Limits
- Default page: 1
- Default limit: 50
- Maximum limit: 100
- Minimum limit: 1

---

## Authentication Standard

### Bearer Token Header
```
Authorization: Bearer {access_token}
```

### Token in URL Query (optional, not recommended)
```
/api/tasks?token={access_token}
```

### Missing/Invalid Token Responses
```json
{
    "error_code": "UNAUTHORIZED",
    "message": "Missing or invalid authentication token",
    "timestamp": "2025-12-14T10:00:00Z"
}
```

---

## Rate Limiting Policy

### Standard Rate Limits
```
/api/auth/login       - 5 requests/minute per IP
/api/auth/signup      - 10 requests/hour per IP
/api/tasks            - 100 requests/minute per user
/api/tasks/{id}       - 1000 requests/minute per user
```

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 75
X-RateLimit-Reset: 1640520000
```

### Rate Limit Exceeded Response
```json
{
    "error_code": "RATE_LIMITED",
    "message": "Too many requests",
    "retry_after": 60,
    "timestamp": "2025-12-14T10:00:00Z"
}
```

---

## Testing Requirements

### Contract Tests
- All endpoints respond with correct status codes
- Request validation works
- Response format matches specification
- Required fields present
- Field types correct

### Integration Tests
- End-to-end workflows (signup → login → create task)
- Authentication enforcement
- Error handling scenarios
- Pagination functionality
- Filtering functionality

### Performance Tests
- Response time targets
- Concurrent requests
- Load handling
- Error rate under load

---

## API Versioning

### Versioning Strategy
- URL path versioning: `/api/v1/tasks`, `/api/v2/tasks`
- Header versioning: `API-Version: 1.0`
- Current version: v1

### Deprecation Policy
- Announce 6 months in advance
- Support old version for 12 months
- Provide migration guide
- Clear deprecation notice in docs

---

## Acceptance Criteria

- [ ] All endpoints specified with examples
- [ ] Request/response formats defined
- [ ] HTTP status codes documented
- [ ] Error codes and messages defined
- [ ] Pagination documented
- [ ] Authentication documented
- [ ] Rate limiting documented
- [ ] OpenAPI schema generated
- [ ] All endpoints contract tested
- [ ] Response validation working
- [ ] Error handling tested
- [ ] Documentation complete

---

## Related Specifications

- `@specs/agents/backend-agent.md` - Backend implementation
- `@specs/agents/frontend-agent.md` - Frontend integration
- `@specs/features/task-crud-web.md` - Task requirements
- `@specs/features/authentication.md` - Auth requirements

---

**Agent Status**: 🔄 Ready for Implementation

**Next Step**: Follow `api-skills.md` for detailed capabilities
