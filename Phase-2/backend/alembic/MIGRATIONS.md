# Database Migrations Guide

## Overview
This directory contains all database schema migrations managed by Alembic. Each migration represents a versioned change to the database schema with an upgrade and downgrade path.

## Migration: 0001_initial_migration

**Revision ID:** 001
**Description:** Create user and task tables with comprehensive indexing strategy
**Created:** 2025-12-14

### Changes

#### User Table
```sql
CREATE TABLE user (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    last_login_at DATETIME
)
```

**Indexes:**
- `ix_user_email` (UNIQUE): Fast email lookups for login and validation. **Why:** Users log in by email; this prevents duplicates and enables O(1) lookup.

#### Task Table
```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR NOT NULL FOREIGN KEY REFERENCES user(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL,
    description VARCHAR,
    status VARCHAR NOT NULL DEFAULT 'Pending',
    priority VARCHAR NOT NULL DEFAULT 'Medium',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    completed_at DATETIME,
    deleted_at DATETIME
)
```

**Indexes:**
1. `ix_task_user_id`: Enables efficient filtering of all tasks for a specific user. **Why:** When loading user dashboard, we query `SELECT * FROM task WHERE user_id = ?`. This is the most common access pattern.

2. `ix_task_title`: Fast search by task title. **Why:** Supports user task search/lookup by name.

3. `ix_task_status`: Filter tasks by status (Pending, In Progress, Completed). **Why:** Kanban-like views need to group by status; this avoids table scans.

4. `ix_task_created_at`: Sort tasks by creation date. **Why:** Task lists often show newest first. Enables efficient ORDER BY without full scan.

5. `ix_task_user_status` (COMPOSITE): Combined (user_id, status) lookup. **Why:** Most common query is "get all tasks for user X with status Y" - this single index answers that query efficiently.

6. Foreign Key Constraint: `task.user_id → user.id` with CASCADE DELETE. **Why:** Multi-user isolation. If user deleted, all their tasks are removed automatically.

### Running Migrations

#### Upgrade to latest version
```bash
cd Phase-2/backend
alembic upgrade head
```

#### Downgrade to specific version
```bash
alembic downgrade 001  # Go back to initial migration state
```

#### Create new migration
For new schema changes, always use autogenerate:
```bash
alembic revision --autogenerate -m "Description of change"
```

#### View migration history
```bash
alembic history
```

#### Current schema version
```bash
alembic current
```

### Database Configuration

Migrations use the `DATABASE_URL` environment variable. Default values:
- **Development (SQLite):** `sqlite:///./test.db`
- **Production (PostgreSQL):** `postgresql://user:password@localhost:5432/task_db`

Set via `.env` file in backend directory.

### Index Strategy Rationale

**Access Pattern Analysis:**
1. **User authentication:** Look up user by email (UNIQUE index)
2. **Load dashboard:** Get all user's tasks (composite index on user_id + status)
3. **Task filtering:** Filter by status/priority (individual status index)
4. **Task search:** Find by title (title index)
5. **Task sorting:** Order by creation date (created_at index)

**Index Count:** 6 indexes total
- Justification: Each index serves a real, documented query pattern
- Trade-off: Small write overhead (INSERT/UPDATE/DELETE) for massive read speedup on SELECT queries

### Multi-User Isolation

The schema enforces data isolation at the database level:
- Every task has a `user_id` foreign key
- Application layer MUST validate user ownership before returning/modifying tasks
- Database enforces referential integrity: task can only reference valid users
- CASCADE DELETE ensures no orphaned tasks if user deleted

### Future Migrations

Planned migrations in Phase 2B will add:
- Audit logging table (task_history)
- Task tags/categories (many-to-many relationship)
- Task templates (reusable task definitions)
- Notification preferences (user notification settings)
