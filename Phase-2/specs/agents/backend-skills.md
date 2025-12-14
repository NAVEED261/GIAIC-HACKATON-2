# Backend Agent Skills

**Agent Name**: Backend Agent (FastAPI/Python Specialist)
**Domain**: Backend - REST API & Business Logic
**Total Skills**: 12 Core + 8 Advanced

---

## Core Skills (Essential for Phase-2)

### 1. REST API Design & Implementation

**Purpose**: Design and implement RESTful endpoints following REST principles

**Example Query**: "Create GET /api/tasks endpoint to list user's tasks"

**Expected Action**:
- Design endpoint with proper HTTP method
- Implement request/response handling
- Follow REST naming conventions
- Return proper status codes
- Document endpoint

**Technical Skills**:
- FastAPI routing (@app.get, @app.post, etc.)
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Status code selection
- Request/response serialization
- Path and query parameters

---

### 2. Request Validation & Pydantic

**Purpose**: Validate incoming requests using Pydantic schemas

**Example Query**: "Validate task creation request has title and valid fields"

**Expected Action**:
- Create Pydantic models for requests
- Define field types and constraints
- Add custom validators
- Return validation errors
- Transform/sanitize input

**Technical Skills**:
- Pydantic BaseModel
- Field validation
- Custom validators (@validator)
- Type hints
- Error handling

---

### 3. Business Logic Implementation

**Purpose**: Implement core business rules and operations

**Example Query**: "Implement task completion logic with status update"

**Expected Action**:
- Create service classes for business logic
- Implement validation rules
- Handle business constraints
- Error handling
- Transaction management

**Technical Skills**:
- Python classes and functions
- Design patterns
- Service layer architecture
- Error handling patterns
- Logging

---

### 4. Database Operations (CRUD)

**Purpose**: Perform Create, Read, Update, Delete operations on database

**Example Query**: "Add task to database and return created task"

**Expected Action**:
- Create database record (INSERT)
- Read records (SELECT)
- Update existing records (UPDATE)
- Delete records (DELETE)
- Handle database constraints

**Technical Skills**:
- SQLModel ORM
- SQLAlchemy queries
- Session management
- Transaction handling
- Constraint enforcement

---

### 5. User Authentication Integration

**Purpose**: Validate JWT tokens and extract current user

**Example Query**: "Extract user ID from JWT token in request"

**Expected Action**:
- Extract token from header
- Validate token signature
- Check token expiration
- Extract user ID from payload
- Handle invalid tokens

**Technical Skills**:
- JWT token handling
- Header parsing
- Token validation
- Payload extraction
- Error responses

---

### 6. Authorization & User Isolation

**Purpose**: Ensure users can only access their own resources

**Example Query**: "Verify user can only see their own tasks"

**Expected Action**:
- Check user ownership
- Filter queries by user_id
- Return 403 Forbidden on violation
- Log unauthorized access
- Handle edge cases

**Technical Skills**:
- Authorization checks
- Ownership verification
- Query filtering
- Error responses
- Audit logging

---

### 7. Error Handling & HTTP Responses

**Purpose**: Handle errors gracefully and return proper HTTP responses

**Example Query**: "Return 404 when task not found"

**Expected Action**:
- Catch exceptions appropriately
- Map errors to HTTP status codes
- Return error responses
- Include error details/messages
- Avoid information leaks

**Technical Skills**:
- Exception handling
- Status code mapping
- Error response formatting
- Logging errors
- Security considerations

---

### 8. Input Sanitization & Security

**Purpose**: Prevent security vulnerabilities like SQL injection, XSS

**Example Query**: "Sanitize task title before storing"

**Expected Action**:
- Validate input length
- Escape special characters
- Prevent injection attacks
- Enforce constraints
- Audit security

**Technical Skills**:
- Input validation
- ORM-based SQL safety
- Length limits
- Type checking
- Security best practices

---

### 9. Pagination & Filtering

**Purpose**: Implement pagination and filtering for list endpoints

**Example Query**: "Implement pagination for task list with limit and offset"

**Expected Action**:
- Accept page/limit parameters
- Calculate offset
- Count total items
- Return paginated results
- Include pagination metadata

**Technical Skills**:
- Query parameters
- LIMIT/OFFSET
- Count queries
- Pagination response format
- Parameter validation

---

### 10. Database Relationships & Joins

**Purpose**: Handle relationships between entities (users and tasks)

**Example Query**: "Get all tasks with user information"

**Expected Action**:
- Define relationships in models
- Perform JOIN queries
- Eager/lazy loading
- Handle cascade operations
- Optimize queries

**Technical Skills**:
- SQLModel relationships
- Foreign keys
- One-to-many relationships
- JOIN queries
- Relationship loading

---

### 11. Middleware & Dependency Injection

**Purpose**: Create middleware for cross-cutting concerns (logging, auth checks)

**Example Query**: "Create middleware to log all requests"

**Expected Action**:
- Create middleware function
- Apply to routes
- Handle request/response
- Extract dependencies
- Error handling

**Technical Skills**:
- FastAPI middleware
- Dependency injection
- Dependency()
- Request/response handling
- Exception handling

---

### 12. Testing & Test Coverage

**Purpose**: Write unit and integration tests for backend code

**Example Query**: "Write test for task creation endpoint"

**Expected Action**:
- Write unit tests for functions
- Write integration tests for endpoints
- Mock database
- Test error cases
- Achieve 80%+ coverage

**Technical Skills**:
- pytest framework
- pytest fixtures
- Mocking (unittest.mock)
- TestClient
- Coverage measurement

---

## Advanced Skills (Optional for Phase-2)

### 13. Async/Await Programming

**Purpose**: Use async operations for I/O-bound tasks

**Example Query**: "Implement async database operations"

**Technical Skills**: async/await, asyncio, async SQLModel operations

---

### 14. Caching Strategies

**Purpose**: Implement caching to improve performance

**Example Query**: "Cache frequently accessed task lists"

**Technical Skills**: Redis caching, in-memory caching, cache invalidation

---

### 15. Rate Limiting & Throttling

**Purpose**: Prevent abuse and control API usage

**Example Query**: "Limit login attempts to 5 per minute"

**Technical Skills**: Rate limiting libraries, token bucket algorithm, per-user limits

---

### 16. Background Jobs & Task Queues

**Purpose**: Run long-running operations asynchronously

**Example Query**: "Send email notifications asynchronously"

**Technical Skills**: Celery, task queues, job scheduling

---

### 17. Database Connection Pooling

**Purpose**: Manage database connections efficiently

**Example Query**: "Configure connection pool for 20 connections"

**Technical Skills**: Connection pooling, pool configuration, lifecycle management

---

### 18. Logging & Monitoring

**Purpose**: Log application events and monitor performance

**Example Query**: "Log all task operations"

**Technical Skills**: Python logging, structured logs, log levels

---

### 19. API Documentation Generation

**Purpose**: Generate automatic API documentation

**Example Query**: "Generate Swagger docs for all endpoints"

**Technical Skills**: OpenAPI/Swagger, FastAPI auto-docs, documentation updates

---

### 20. Data Migration & Seeding

**Purpose**: Create and manage database migrations and test data

**Example Query**: "Create migration to add priority field to tasks"

**Technical Skills**: Alembic migrations, seed scripts, rollback strategies

---

## Skill Composition Example

### User Workflow: Create Task
```
1. User sends POST request with task data
2. Validate request (Skill #2: Pydantic Validation)
3. Extract user from token (Skill #5: Authentication)
4. Implement business logic (Skill #3: Business Logic)
5. Save to database (Skill #4: CRUD Operations)
6. Check user authorization (Skill #6: User Isolation)
7. Handle errors (Skill #7: Error Handling)
8. Return response (Skill #1: REST API)
9. Log operation (Skill #18: Logging)
10. Test endpoint (Skill #12: Testing)
```

---

## Skill Dependencies

```
REST API Design (#1)
    ├─ Request Validation (#2)
    ├─ Business Logic (#3)
    ├─ CRUD Operations (#4)
    ├─ Error Handling (#7)
    └─ Testing (#12)

Authentication (#5)
    ├─ Request Validation (#2)
    ├─ Error Handling (#7)
    ├─ Middleware (#11)
    └─ Testing (#12)

Authorization (#6)
    ├─ Authentication (#5)
    ├─ Database Relationships (#10)
    ├─ Error Handling (#7)
    └─ Testing (#12)

CRUD Operations (#4)
    ├─ Database Relationships (#10)
    ├─ Pagination (#9)
    ├─ Error Handling (#7)
    └─ Testing (#12)

Business Logic (#3)
    ├─ Request Validation (#2)
    ├─ CRUD Operations (#4)
    ├─ Authorization (#6)
    ├─ Input Sanitization (#8)
    └─ Testing (#12)
```

---

## Guardrails

### Must Do
- ✅ Use type hints for all functions
- ✅ Validate all input with Pydantic
- ✅ Check user authorization on protected routes
- ✅ Log security-relevant events
- ✅ Test all endpoints and business logic
- ✅ Handle exceptions gracefully
- ✅ Never hardcode secrets

### Must Not Do
- ❌ Expose sensitive error details to clients
- ❌ Trust user input without validation
- ❌ Perform operations without user authorization check
- ❌ Leave unhandled exceptions
- ❌ Write untested code
- ❌ Use raw SQL queries (use ORM)
- ❌ Log passwords or sensitive data

### Out of Scope
- Web scraping
- Advanced async patterns (Phase-3+)
- Blockchain/cryptocurrency features
- Machine learning (Phase-5+)
- Complex caching strategies (optional)
- Event streaming (Phase-5+)

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **API Response Time** | < 500ms (p95) |
| **Database Query Time** | < 100ms (p95) |
| **Test Coverage** | ≥ 80% |
| **Endpoint Availability** | 99.5%+ |
| **Error Rate** | < 0.1% |
| **Test Pass Rate** | 100% |

---

**Skill Status**: Ready for use by Backend Agent

**Related**: backend-agent.md, backend-agent tasks
