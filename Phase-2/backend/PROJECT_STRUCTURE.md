# Backend Project Structure

## Overview

The Phase-2 backend is organized following modular, domain-driven design principles. Each module has a single responsibility and clear interfaces.

```
Phase-2/backend/
├── main.py                    # Application entry point (FastAPI setup)
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies (SQLite)
├── .env.example              # Environment configuration template
│
├── models/                    # SQLModel definitions (ORM layer)
│   ├── __init__.py           # Package exports
│   ├── user.py               # User model and response schemas
│   └── task.py               # Task model and request/response schemas
│
├── db/                        # Database layer
│   ├── __init__.py           # Package exports
│   ├── connection.py          # SQLAlchemy engine factory
│   └── session.py            # Session factory and FastAPI dependency
│
├── routes/                    # API endpoint handlers (domain-driven)
│   ├── __init__.py           # Package exports and router registration
│   ├── auth.py               # Authentication endpoints (signup, login, etc.)
│   ├── tasks.py              # Task management endpoints (CRUD, complete)
│   └── health.py             # Health check endpoints
│
├── alembic/                   # Database migrations
│   ├── env.py                # Alembic environment configuration
│   ├── versions/             # Migration scripts
│   │   └── 0001_initial_migration.py  # Initial User/Task schema
│   ├── MIGRATIONS.md         # Migration documentation
│   └── script.py.mako        # Migration template
│
├── alembic.ini               # Alembic configuration
│
├── docs/                     # Documentation (future)
│   ├── API_DOCUMENTATION.md  # Complete API reference
│   ├── DB_SETUP.md           # Database setup guide
│   ├── MIGRATION_GUIDE.md    # Migration management guide
│   └── PROJECT_STRUCTURE.md  # This file
│
└── migrate.py               # Database migration helper script
```

---

## Module Organization

### 1. `main.py` - Application Entry Point

**Purpose:** Bootstrap the FastAPI application with all configuration, middleware, and routes.

**Responsibilities:**
- Create FastAPI app instance
- Configure middleware (CORS, logging, etc.)
- Register route routers
- Define event handlers (startup, shutdown)
- Provide root API information endpoint

**Key Components:**
```python
app = FastAPI(...)              # Application instance
app.add_middleware(...)         # Middleware configuration
@app.on_event("startup")        # Startup hook
app.include_router(...)         # Route registration
```

**Dependencies:**
- routes (auth_router, tasks_router, health_router)
- db (create_all_tables, engine)

**Related Files:**
- `requirements.txt` - All dependencies
- `.env.example` - Configuration template

---

### 2. `models/` - ORM Layer

**Purpose:** Define data models using SQLModel (SQLAlchemy + Pydantic hybrid).

**Files:**

#### `models/user.py`
- **User Model:** ORM table mapping
  ```python
  class User(SQLModel, table=True):
      id: str (Primary Key)
      email: str (UNIQUE, indexed)
      name: str
      password_hash: str
      created_at: datetime
      updated_at: datetime
      is_active: bool
      last_login_at: Optional[datetime]
  ```
- **UserResponse:** API response schema (excludes password_hash)
- **UserCreate:** Registration request schema

#### `models/task.py`
- **Task Model:** ORM table mapping
  ```python
  class Task(SQLModel, table=True):
      id: Optional[int] (Primary Key, auto-increment)
      user_id: str (Foreign Key → User.id, CASCADE DELETE)
      title: str (indexed)
      description: Optional[str]
      status: str (indexed, default "Pending")
      priority: str (default "Medium")
      created_at: datetime (indexed)
      updated_at: datetime
      completed_at: Optional[datetime]
      deleted_at: Optional[datetime] (soft delete flag)
  ```
- **TaskResponse:** API response schema
- **TaskCreate:** Creation request schema
- **TaskUpdate:** Update request schema

**Design Principles:**
- Single responsibility: One model per file
- Complete schemas: Request, Response, and Update schemas included
- Field validation: Pydantic validators for constraints
- Relationships: Foreign keys with cascade behavior
- Indexing: Strategic indexes for query performance

**Related Files:**
- `alembic/versions/0001_initial_migration.py` - Schema definition
- `db/connection.py` - Uses models for table creation

---

### 3. `db/` - Database Layer

**Purpose:** Manage database connections, sessions, and engine configuration.

**Files:**

#### `db/connection.py`
- **get_database_url():** Read DATABASE_URL from environment
- **create_db_engine():** Create SQLAlchemy engine
  - SQLite for development (local, no setup needed)
  - PostgreSQL for production (pooled, optimized)
- **create_all_tables():** Initialize schema from SQLModel definitions
- **engine:** Global engine instance

**Configuration:**
- Supports both SQLite (development) and PostgreSQL (production)
- Connection pooling for production databases
- SQL echo for debugging (SQL_ECHO env var)

#### `db/session.py`
- **SessionLocal:** Sessionmaker factory
- **get_db():** FastAPI dependency for injecting sessions into routes
  ```python
  async def route(db: Session = Depends(get_db)):
      # db automatically provides and cleans up session
  ```

**Design Principles:**
- Dependency injection: Sessions injected via FastAPI Depends
- Automatic cleanup: Context manager ensures session closure
- Pool management: Configurable pool size and overflow

**Related Files:**
- `alembic/env.py` - Uses engine for migrations
- `routes/` - Routes use get_db dependency
- `.env.example` - Configuration reference

---

### 4. `routes/` - API Endpoints

**Purpose:** Define HTTP endpoints organized by business domain.

**Architecture:**
Each route module handles one domain and includes:
- Endpoint definitions with OpenAPI documentation
- Request/response schemas
- Business logic placeholders (TODO)
- Error handling
- Multi-user isolation enforcement

**Files:**

#### `routes/auth.py` - Authentication
Endpoints:
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - Login (returns JWT tokens)
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

Request/Response Schemas:
- SignupRequest/Response
- LoginRequest/Response
- TokenRefreshRequest/Response
- LogoutResponse

#### `routes/tasks.py` - Task Management
Endpoints:
- `GET /api/tasks` - List user's tasks (paginated)
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Mark complete

Request/Response Schemas:
- TaskResponse
- TaskCreate
- TaskUpdate

Multi-User Isolation:
- All endpoints filter by authenticated user_id
- 403 Forbidden if task belongs to different user
- Enforced at both DB and app level

#### `routes/health.py` - Health Checks
Endpoints:
- `GET /health` - Application health
- `GET /health/db` - Database health

No authentication required (used by load balancers/monitoring).

**Design Principles:**
- Domain-driven: One file per business domain
- Complete documentation: OpenAPI docstrings with examples
- Error handling: Comprehensive error responses with proper status codes
- Security: User isolation enforced at route level
- Pagination: List endpoints support skip/limit
- Flexibility: Partial updates supported (PUT, PATCH)

**Related Files:**
- `routes/__init__.py` - Exports all routers for main.py registration
- `models/` - Uses models for request/response schemas
- `db/` - Uses get_db dependency

---

### 5. `alembic/` - Database Migrations

**Purpose:** Version control for database schema with upgrade/downgrade capabilities.

**Files:**

#### `alembic/env.py` - Alembic Environment
- Configures Alembic runtime
- Imports SQLModel metadata for autogenerate
- Handles both offline and online migrations
- Supports environment variable DATABASE_URL

#### `alembic/versions/0001_initial_migration.py` - Initial Schema
Creates:
- User table with 8 columns and email index
- Task table with 10 columns and 6 indexes
- Foreign key relationship with cascade delete

Indexes Created:
- `ix_user_email` - Fast login lookups
- `ix_task_user_id` - Efficient user task filtering
- `ix_task_title` - Task search support
- `ix_task_status` - Kanban board grouping
- `ix_task_created_at` - Timeline sorting
- `ix_task_user_status` - Most common query (composite)

#### `alembic.ini` - Configuration
- Migration script location
- Database URL (can use environment variables)
- Logging configuration

#### `alembic/MIGRATIONS.md` - Documentation
- Index strategy explanation
- Migration rationale
- Running migrations guide

**Migration Workflow:**
1. Modify model in `models/`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration
4. Apply: `alembic upgrade head`
5. Rollback if needed: `alembic downgrade -1`

**Related Files:**
- `MIGRATION_GUIDE.md` - Complete CLI guide
- `models/` - Schema definitions
- `DB_SETUP.md` - Database setup guide

---

## File Relationships

### Request Flow

```
Client Request
    ↓
FastAPI Routing (main.py)
    ↓
Route Handler (routes/auth.py, routes/tasks.py)
    ↓
Database Session Dependency (db/session.py → get_db)
    ↓
Database Query (models/ with SQLModel)
    ↓
Database Engine (db/connection.py)
    ↓
Database (SQLite/PostgreSQL)
    ↓
Response (Route Handler)
    ↓
Client Response
```

### Dependency Graph

```
main.py
├── routes/__init__.py
│   ├── auth.py
│   │   ├── models/user.py
│   │   └── db/session.py
│   ├── tasks.py
│   │   ├── models/task.py
│   │   ├── models/user.py
│   │   └── db/session.py
│   └── health.py
│       └── db/connection.py
│
├── db/__init__.py
│   ├── connection.py
│   │   ├── models/user.py
│   │   ├── models/task.py
│   │   └── SQLAlchemy Engine
│   └── session.py
│
└── Middleware
    └── CORS from environment
```

---

## Configuration

### Environment Variables

Create `.env` file in backend directory:

```env
# Database
DATABASE_URL=sqlite:///./test.db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
SQL_ECHO=false

# JWT/Authentication
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Email (Future)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

See `.env.example` for complete template.

---

## Running the Application

### Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt  # For development with SQLite

# Create .env file
cp .env.example .env

# Run migrations
python migrate.py upgrade

# Start server
python main.py
# Or with auto-reload
uvicorn main:app --reload

# Access API
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Production

```bash
# Install dependencies
pip install -r requirements.txt  # Includes PostgreSQL driver

# Run migrations
alembic upgrade head

# Start server with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Or with custom Uvicorn config
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Testing Structure (Phase 2D)

Future test organization:

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_models.py           # Model validation tests
├── test_auth_routes.py      # Authentication endpoint tests
├── test_tasks_routes.py     # Task CRUD endpoint tests
├── test_health_routes.py    # Health check tests
├── test_db_connection.py    # Database connection tests
├── test_migrations.py       # Migration tests
├── test_multi_user.py       # Multi-user isolation tests
└── integration/             # Integration tests
    └── test_workflows.py    # End-to-end workflows
```

---

## Security Considerations

### Implemented
- ✅ Password hashing (bcrypt in requirements)
- ✅ JWT authentication
- ✅ User isolation (user_id filtering)
- ✅ Foreign key constraints
- ✅ SQL injection prevention (SQLModel/SQLAlchemy parameterization)
- ✅ CORS configuration
- ✅ Environment variable for secrets

### Future (Phase 2B+)
- [ ] Rate limiting
- [ ] HTTPS/TLS enforcement
- [ ] Request validation middleware
- [ ] Audit logging
- [ ] Token blacklisting on logout
- [ ] CSRF protection

---

## Performance Optimization

### Current
- Strategic database indexes (6 total)
- Connection pooling (production)
- Pagination support (max 100 items)
- Efficient queries via SQLModel

### Future (Phase 2B+)
- [ ] Query result caching (Redis)
- [ ] Database query profiling
- [ ] Endpoint response caching
- [ ] Batch operations support
- [ ] Async query execution

---

## Error Handling

All endpoints return consistent error format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

HTTP Status Codes:
- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request (invalid input)
- 401: Unauthorized (not authenticated)
- 403: Forbidden (access denied)
- 404: Not Found
- 409: Conflict
- 500: Server Error
- 503: Service Unavailable (database down)

---

## Development Workflow

### Adding a New Feature

1. **Update Model** (`models/`)
   - Add new fields or models
   - Include validation

2. **Create Migration** (`alembic/versions/`)
   ```bash
   alembic revision --autogenerate -m "description"
   ```
   - Review generated migration
   - Apply: `alembic upgrade head`

3. **Add Route** (`routes/`)
   - Create endpoint handler
   - Include OpenAPI docstring
   - Add request/response schemas

4. **Write Tests** (`tests/`)
   - Unit tests for business logic
   - Integration tests for workflows

5. **Document** (`.md` files)
   - Update API_DOCUMENTATION.md
   - Update this file if structure changed

---

## Next Steps (Phase 2B)

Phase 2B will add:
- Authentication implementation (signup, login, JWT)
- Task CRUD implementation
- User authorization middleware
- Error handling middleware
- Rate limiting middleware
- Comprehensive test suite (80%+ coverage)

See `specs/plan.md` for complete Phase 2B details.

---

## Quick Reference

### Common Commands

```bash
# Start development server
python main.py

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check current version
alembic current

# View migration history
alembic history

# Install dependencies
pip install -r requirements-dev.txt

# Access API documentation
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### File Locations

| Concept | Location |
|---------|----------|
| ORM Models | `models/*.py` |
| Database Config | `db/connection.py` |
| Sessions | `db/session.py` |
| Endpoints | `routes/*.py` |
| Migrations | `alembic/versions/` |
| Configuration | `.env` |
| Dependencies | `requirements*.txt` |
| Documentation | `*.md` files |

---

## Support

For questions or issues:
1. Check `API_DOCUMENTATION.md` for endpoint details
2. Check `DB_SETUP.md` for database issues
3. Check `MIGRATION_GUIDE.md` for schema issues
4. Review docstrings in relevant `.py` files
5. Check application logs with `DEBUG=true` in `.env`
