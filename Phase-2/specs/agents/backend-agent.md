# Backend Agent Specification

**Agent Name**: Backend Agent (FastAPI/Python Specialist)
**Domain**: Backend - REST API & Business Logic
**Technology**: Python 3.8+, FastAPI, SQLModel, Pydantic
**Responsibility**: Build RESTful API and implement business logic
**Created**: 2025-12-14

---

## Agent Overview

The Backend Agent is responsible for designing, building, and maintaining the REST API, business logic, and backend services of the Phase-2 full-stack application.

### Primary Responsibilities

1. **REST API Development**
   - Design RESTful endpoints following best practices
   - Implement CRUD operations for tasks
   - Handle authentication and authorization
   - Return proper HTTP status codes
   - Document API endpoints (OpenAPI/Swagger)

2. **Business Logic**
   - Task validation and constraints
   - User isolation and data security
   - Error handling and recovery
   - Transaction management
   - Rate limiting and throttling

3. **Database Integration**
   - Model design with SQLModel
   - Database migrations
   - Query optimization
   - Connection pooling
   - Transaction handling

4. **Authentication**
   - JWT token validation
   - User identification from tokens
   - Permission checking
   - Session management
   - Token refresh logic

5. **Testing**
   - Unit tests for business logic
   - Integration tests for API endpoints
   - Database tests
   - Authentication tests
   - Performance tests

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | FastAPI | REST API framework |
| **Language** | Python 3.8+ | Backend language |
| **ORM** | SQLModel | Database ORM |
| **Validation** | Pydantic | Data validation |
| **Database** | Neon PostgreSQL | Data persistence |
| **Auth** | PyJWT | JWT handling |
| **Testing** | pytest | Unit & integration tests |
| **Documentation** | OpenAPI/Swagger | API docs |
| **CORS** | fastapi-cors | Cross-origin handling |

---

## Deliverables

### API Routes (routes/ directory)
- `routes/tasks.py` - Task CRUD endpoints
- `routes/auth.py` - Authentication endpoints
- `routes/health.py` - Health check endpoints
- `routes/users.py` - User endpoints

### Models (models/ directory)
- `models/task.py` - Task SQLModel
- `models/user.py` - User model
- `models/schemas.py` - Pydantic schemas
- `models/enums.py` - Enum definitions

### Database (db/ directory)
- `db.py` - Database connection
- `session.py` - Session management
- `migrations/` - Alembic migrations
- `seed.py` - Test data seeding

### Middleware & Utils
- `middleware/auth.py` - JWT validation
- `middleware/cors.py` - CORS handling
- `utils/security.py` - Security helpers
- `utils/validation.py` - Validation helpers
- `config.py` - Configuration
- `main.py` - FastAPI app setup

### Testing (tests/ directory)
- `tests/test_tasks.py` - Task endpoint tests
- `tests/test_auth.py` - Auth endpoint tests
- `tests/test_db.py` - Database tests
- `tests/conftest.py` - Test fixtures

---

## API Endpoints to Implement

### Task Endpoints
```
GET    /api/tasks                 # List user's tasks
POST   /api/tasks                 # Create new task
GET    /api/tasks/{id}            # Get task details
PUT    /api/tasks/{id}            # Update task
DELETE /api/tasks/{id}            # Delete task
PATCH  /api/tasks/{id}/complete   # Toggle completion
```

### Auth Endpoints
```
POST   /api/auth/signup           # User registration
POST   /api/auth/login            # User login
POST   /api/auth/logout           # User logout
POST   /api/auth/refresh          # Refresh JWT token
GET    /api/auth/me               # Get current user
```

### Health Endpoints
```
GET    /health                    # Health check
GET    /health/db                 # Database health
```

---

## Data Models

### Task Model
```python
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str
    description: str | None = None
    status: str = "Pending"  # Pending, Completed
    created_at: datetime
    updated_at: datetime
```

### TaskSchema (Pydantic)
```python
class TaskCreate(BaseModel):
    title: str  # 1-200 chars
    description: str | None = None  # max 1000 chars

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime
```

---

## Key Features to Implement

### 1. CRUD Operations
- Create task with validation
- Read single/multiple tasks
- Update task with partial updates
- Delete task with cascade
- List with pagination and filtering

### 2. Authentication
- JWT token validation
- Extract user_id from token
- Check token expiration
- Validate JWT signature
- Handle missing/invalid tokens

### 3. User Isolation
- Filter all queries by user_id
- Prevent cross-user access
- Check ownership before modify
- Return 403 Forbidden on violation
- Log unauthorized access attempts

### 4. Input Validation
- Validate title (required, 1-200 chars)
- Validate description (max 1000 chars)
- Validate status (enum: Pending, Completed)
- Validate IDs (integer, exists)
- Sanitize inputs

### 5. Error Handling
- 400 Bad Request - invalid input
- 401 Unauthorized - missing/invalid token
- 403 Forbidden - insufficient permissions
- 404 Not Found - resource doesn't exist
- 422 Unprocessable Entity - validation error
- 500 Internal Server Error - server error

### 6. Response Formatting
- Consistent JSON format
- Include error messages
- Include timestamps
- Include resource IDs
- Include pagination info

### 7. Performance
- Database indexes on user_id
- Connection pooling
- Query optimization
- Pagination (limit 100)
- Caching (if needed)

### 8. Security
- SQL injection prevention (via ORM)
- XSS prevention (via Pydantic)
- CSRF token handling
- Rate limiting
- Input length limits
- Timeout handling

---

## Database Schema

### Tables
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

---

## API Response Examples

### Success Response
```json
{
    "id": 1,
    "user_id": "user_123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "Pending",
    "created_at": "2025-12-14T10:00:00Z",
    "updated_at": "2025-12-14T10:00:00Z"
}
```

### Error Response
```json
{
    "error_code": "VALIDATION_ERROR",
    "message": "Invalid task title",
    "details": {
        "field": "title",
        "error": "Title must be 1-200 characters"
    }
}
```

### List Response
```json
{
    "data": [
        { "id": 1, "title": "Task 1", "status": "Pending" },
        { "id": 2, "title": "Task 2", "status": "Completed" }
    ],
    "count": 2,
    "total": 5,
    "page": 1,
    "limit": 50
}
```

---

## Testing Requirements

### Unit Tests
- Model validation
- Business logic functions
- Helper utilities
- Validation functions

### Integration Tests
- API endpoint behavior
- Database CRUD operations
- Authentication flow
- Authorization checks
- Error handling

### Database Tests
- Connection pooling
- Transaction rollback
- Cascade deletes
- Index performance
- Query optimization

### Authentication Tests
- Valid token acceptance
- Invalid token rejection
- Expired token handling
- Missing token handling
- User isolation enforcement

---

## Performance Targets

| Metric | Target |
|--------|--------|
| **Response Time** | < 500ms (p95) |
| **Database Query** | < 100ms (p95) |
| **Concurrent Users** | 1,000+ |
| **Requests/Second** | 1,000+ |
| **Test Coverage** | ≥ 80% |
| **Uptime** | 99.5% |

---

## Configuration

### Environment Variables
```
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your_secret_key
JWT_EXPIRY_DAYS=7
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
CORS_ORIGINS=http://localhost:3000
```

---

## Acceptance Criteria

- [ ] All 6 API endpoints working
- [ ] JWT authentication enforced
- [ ] User isolation implemented
- [ ] Input validation working
- [ ] Error responses correct
- [ ] Database queries optimized
- [ ] All tests passing (≥80% coverage)
- [ ] API documentation complete
- [ ] Performance targets met
- [ ] Security best practices followed
- [ ] No SQL injection vulnerabilities
- [ ] Proper error logging

---

## Related Specifications

- `@specs/features/authentication.md` - Auth requirements
- `@specs/features/task-crud-web.md` - CRUD requirements
- `@specs/api/rest-endpoints.md` - API contracts
- `@specs/database/schema.md` - Database schema

---

**Agent Status**: 🔄 Ready for Implementation

**Next Step**: Follow `backend-skills.md` for detailed capabilities
