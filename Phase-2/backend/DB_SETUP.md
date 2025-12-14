# Database Setup and Migration Guide

## Overview

The Phase-2 backend uses:
- **SQLModel** for ORM (combines SQLAlchemy + Pydantic)
- **Alembic** for schema versioning and migrations
- **PostgreSQL** for production (supports SQLite for development)
- **SQLAlchemy** as the database engine

This guide explains the complete database setup, migration strategy, and index design.

## Quick Start

### 1. Environment Setup
Create `.env` file in `Phase-2/backend/`:

**For Development (SQLite):**
```env
DATABASE_URL=sqlite:///./test.db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
SQL_ECHO=false
JWT_SECRET_KEY=dev-secret-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

**For Production (PostgreSQL):**
```env
DATABASE_URL=postgresql://user:password@db.example.com:5432/task_db
# ... rest of config
```

### 2. Install Dependencies

**Development (with SQLite):**
```bash
cd Phase-2/backend
pip install -r requirements-dev.txt
```

**Production (includes PostgreSQL driver):**
```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Or use the helper script
python migrate.py upgrade
```

### 4. Start the Application

```bash
# With auto-reload (development)
python main.py

# Or manually
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Database Schema

### User Table
```
id (VARCHAR, PK)
├── email (VARCHAR, UNIQUE, INDEXED) - Login identifier
├── name (VARCHAR) - Display name
├── password_hash (VARCHAR) - Bcrypt hash
├── created_at (DATETIME) - Account creation time
├── updated_at (DATETIME) - Last modified time
├── is_active (BOOLEAN) - Account status (default: true)
└── last_login_at (DATETIME) - Last login timestamp
```

**Relationships:**
- 1:N with Task (CASCADE DELETE)

### Task Table
```
id (INTEGER PK, AUTOINCREMENT)
├── user_id (VARCHAR, FK → user.id, INDEXED)
├── title (VARCHAR, INDEXED)
├── description (VARCHAR)
├── status (VARCHAR, INDEXED) - "Pending", "In Progress", "Completed"
├── priority (VARCHAR) - "Low", "Medium", "High"
├── created_at (DATETIME, INDEXED)
├── updated_at (DATETIME)
├── completed_at (DATETIME) - When task marked complete
└── deleted_at (DATETIME) - Soft delete flag
```

**Relationships:**
- N:1 with User (CASCADE DELETE)

## Index Strategy

### Index Design Rationale

| Index | Table | Columns | Query Pattern | Performance |
|-------|-------|---------|---------------|-------------|
| `ix_user_email` | user | email | Login by email | O(1) exact match |
| `ix_task_user_id` | task | user_id | User dashboard load | O(n) where n = user's tasks |
| `ix_task_title` | task | title | Search tasks by name | Prefix or full-text search |
| `ix_task_status` | task | status | Filter by status | Group by status (Kanban) |
| `ix_task_created_at` | task | created_at | Sort by date | ORDER BY without scan |
| `ix_task_user_status` | task | (user_id, status) | **Most common query** | User's tasks by status |

### Why These Indexes?

**Access Pattern Analysis:**

1. **User Authentication (Very Frequent)**
   ```sql
   SELECT * FROM user WHERE email = ?
   ```
   Index: `ix_user_email` (UNIQUE)
   Avoids: O(n) full table scan

2. **Load User Dashboard (Very Frequent)**
   ```sql
   SELECT * FROM task WHERE user_id = ? AND status = ?
   ```
   Index: `ix_task_user_status` (composite)
   Avoids: Full table scan, then filtering

3. **Task Search (Frequent)**
   ```sql
   SELECT * FROM task WHERE user_id = ? AND title LIKE ?
   ```
   Indexes: `ix_task_user_id`, `ix_task_title`
   Avoids: Full table scan

4. **Kanban Board View (Frequent)**
   ```sql
   SELECT * FROM task WHERE user_id = ? AND status IN ('Pending', 'In Progress')
   ```
   Indexes: `ix_task_status`, `ix_task_user_status`
   Avoids: Full table scan

5. **Task Timeline (Occasional)**
   ```sql
   SELECT * FROM task WHERE user_id = ? ORDER BY created_at DESC
   ```
   Index: `ix_task_created_at`
   Avoids: Full table scan then sort

### Total Index Count: 6
- **Justification:** Each index serves a real, documented query pattern
- **Trade-off:** Write overhead (INSERT/UPDATE/DELETE) is minimal for read-heavy workload
- **Cost:** ~5-10% disk space overhead per table, worth the query speedup

## Migrations

### Migration: 0001_initial_migration
- **Location:** `alembic/versions/0001_initial_migration.py`
- **What it does:**
  - Creates `user` table with 8 columns
  - Creates `task` table with 10 columns
  - Establishes foreign key relationship
  - Creates all 6 indexes
  - Defines CASCADE DELETE behavior

### Running Migrations

**View current version:**
```bash
alembic current
```

**View all migrations:**
```bash
alembic history
```

**Apply pending migrations:**
```bash
alembic upgrade head
```

**Revert last migration:**
```bash
alembic downgrade -1
```

**Revert to specific version:**
```bash
alembic downgrade 001
```

## Multi-User Data Isolation

### Database Level
1. Every task has `user_id` foreign key
2. Foreign key constraint prevents orphaned tasks
3. CASCADE DELETE removes all user's tasks when user deleted

### Application Level
1. **Authentication:** Users identified by JWT token
2. **Authorization:** Extract `user_id` from token
3. **Query Filtering:** ALWAYS filter by `user_id`
4. **Example:**
   ```python
   @app.get("/api/tasks")
   async def list_tasks(db: Session = Depends(get_db),
                       user_id: str = Depends(get_current_user)):
       # CRITICAL: Filter by user_id to prevent data leakage
       tasks = db.query(Task).filter(Task.user_id == user_id).all()
       return tasks
   ```

### Constraints Enforced
- User can only see their own tasks
- User cannot modify other users' tasks
- Deleting user automatically removes their tasks
- No orphaned tasks possible

## Performance Characteristics

### Query Performance with Indexes

**Without indexes:** Millions of users, billions of tasks
- User login: O(n) = 1 billion operations 🔴
- Load dashboard: O(n) = 1 billion operations 🔴
- Search tasks: O(n) = 1 billion operations 🔴

**With our indexes:** Same scale
- User login: O(1) = 1 operation ✅
- Load dashboard: O(m) where m = user's tasks (typically <100) ✅
- Search tasks: O(m) ✅

### Storage Overhead

Per table:
- **User table:** ~1KB per user
  - 1M users = ~1GB
  - Indexes = ~50MB (5% overhead)

- **Task table:** ~200B per task
  - 1B tasks = ~200GB
  - Indexes = ~10GB (5% overhead)

**Conclusion:** Disk overhead minimal compared to query performance gain.

## Development Workflow

### Adding a New Column

1. **Modify Model:**
   ```python
   # In models/task.py
   class Task(SQLModel, table=True):
       # ... existing fields
       new_field: str = Field(...)  # NEW
   ```

2. **Create Migration:**
   ```bash
   alembic revision --autogenerate -m "Add new_field to task"
   ```

3. **Review Migration:**
   - Check `alembic/versions/` for generated file
   - Ensure `upgrade()` and `downgrade()` look correct

4. **Apply Migration:**
   ```bash
   alembic upgrade head
   ```

5. **Test:**
   - Start app: `python main.py`
   - Verify new field works

### Adding an Index

1. **Modify Migration File:**
   ```python
   def upgrade() -> None:
       op.create_index("ix_task_field", "task", ["field"])

   def downgrade() -> None:
       op.drop_index("ix_task_field", table_name="task")
   ```

2. **Apply:**
   ```bash
   alembic upgrade head
   ```

## Troubleshooting

### "No such table: user"
**Cause:** Migrations not applied
**Fix:**
```bash
alembic upgrade head
```

### "Column already exists"
**Cause:** Migration ran twice (idempotency issue)
**Fix:**
```bash
# Check alembic_version table
alembic history
alembic current
# May need manual recovery
```

### "Can't connect to database"
**Cause:** DATABASE_URL invalid or service down
**Fix:**
```bash
# Verify .env file
cat .env | grep DATABASE_URL

# For PostgreSQL, check server is running
psql -U user -h host -d task_db
```

### "Permission denied" (SQLite)
**Cause:** No write permissions in directory
**Fix:**
```bash
# Ensure write permissions
chmod 755 .
```

## Files Reference

```
Phase-2/backend/
├── models/
│   ├── __init__.py         - Exports all models
│   ├── user.py             - User model definition
│   └── task.py             - Task model definition
├── db/
│   ├── __init__.py         - DB module exports
│   ├── connection.py        - Engine factory
│   └── session.py          - Session management
├── alembic/
│   ├── env.py              - Alembic environment
│   ├── versions/
│   │   └── 0001_initial_migration.py  - Initial schema
│   ├── MIGRATIONS.md       - Migration documentation
│   └── script.py.mako      - Migration template
├── alembic.ini             - Alembic configuration
├── main.py                 - FastAPI app entry
├── requirements.txt        - Production dependencies
├── requirements-dev.txt    - Development dependencies
├── .env.example            - Environment template
├── DB_SETUP.md             - This file
└── MIGRATION_GUIDE.md      - Migration CLI guide
```

## Next Steps

Phase 2B will likely add:
- [ ] Task history table (audit log)
- [ ] Task tags/categories (many-to-many)
- [ ] User notifications settings
- [ ] Task time tracking
- [ ] Task subtasks/dependencies

Each addition follows the same pattern:
1. Add model(s)
2. Create migration
3. Test upgrade/downgrade
4. Update this documentation
