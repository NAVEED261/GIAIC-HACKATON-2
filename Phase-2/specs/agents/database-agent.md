# Database Agent Specification

**Agent Name**: Database Agent (PostgreSQL Specialist)
**Domain**: Database - Data Persistence & Schema Management
**Technology**: PostgreSQL, SQLModel, Alembic, SQLAlchemy
**Responsibility**: Design, manage, and optimize database schema and operations
**Created**: 2025-12-14

---

## Agent Overview

The Database Agent is responsible for designing, implementing, and maintaining the PostgreSQL database schema, migrations, and data persistence layer of the Phase-2 full-stack application.

### Primary Responsibilities

1. **Schema Design**
   - Design normalized database schema
   - Define tables for users, tasks, and related entities
   - Create proper relationships with foreign keys
   - Implement constraints (UNIQUE, NOT NULL, CHECK)
   - Design for scalability and performance

2. **Migrations Management**
   - Create Alembic migration scripts
   - Handle schema version control
   - Implement rollback strategies
   - Track schema evolution over time
   - Document migration purposes

3. **Query Optimization**
   - Create appropriate database indexes
   - Analyze and optimize slow queries
   - Design efficient query patterns
   - Implement query result caching strategies
   - Monitor query performance

4. **Data Integrity**
   - Implement referential integrity constraints
   - Handle cascade deletes properly
   - Validate data constraints
   - Implement audit trails (created_at, updated_at)
   - Ensure data consistency across operations

5. **Connection Management**
   - Configure connection pooling
   - Implement connection lifecycle management
   - Handle connection timeouts and retries
   - Monitor active connections
   - Implement proper connection cleanup

6. **Testing**
   - Unit tests for schema definition
   - Integration tests for data operations
   - Migration rollback tests
   - Performance tests for queries
   - Data integrity tests

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Database** | PostgreSQL 14+ | Relational database |
| **ORM** | SQLModel | SQLAlchemy wrapper with Pydantic |
| **Migrations** | Alembic | Schema version control |
| **Connection** | asyncpg / psycopg2 | Database driver |
| **Pooling** | SQLAlchemy Pool | Connection pooling |
| **Testing** | pytest | Database tests |

---

## Deliverables

### Models (models/ directory)
- `models/user.py` - User SQLModel with relationships
- `models/task.py` - Task SQLModel with relationships
- `models/base.py` - Base model with common fields
- `models/__init__.py` - Model exports

### Database (db/ directory)
- `db/connection.py` - Database connection setup
- `db/session.py` - Session factory and management
- `db/engine.py` - SQLEngine configuration
- `db/pool.py` - Connection pool configuration

### Migrations (db/migrations/ directory)
- `alembic.ini` - Alembic configuration
- `db/migrations/versions/` - Migration scripts
- `db/migrations/env.py` - Migration environment
- `db/migrations/script.py.mako` - Migration template

### Schema (db/schema/ directory)
- `db/schema/users.sql` - User table SQL
- `db/schema/tasks.sql` - Task table SQL
- `db/schema/indexes.sql` - Index definitions
- `db/schema/constraints.sql` - Constraint definitions

### Testing (tests/db/ directory)
- `tests/db/test_models.py` - Model validation tests
- `tests/db/test_migrations.py` - Migration tests
- `tests/db/test_queries.py` - Query optimization tests
- `tests/db/test_integrity.py` - Data integrity tests
- `tests/db/conftest.py` - Database test fixtures

### Documentation
- `db/README.md` - Database setup and usage
- `db/SCHEMA.md` - Schema documentation
- `db/MIGRATIONS.md` - Migration guide

---

## Database Schema

### Tables

#### Users Table
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMP NULL
);

CREATE INDEX idx_users_email ON users(email);
```

#### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    priority VARCHAR(20) DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

### Relationships

```
users (1) ─────────── (N) tasks
  id (PK)             user_id (FK)
```

- One user has many tasks
- Deleting a user cascades to their tasks
- Tasks are isolated per user

---

## SQLModel Definitions

### User Model
```python
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    last_login_at: Optional[datetime] = None

    tasks: List["Task"] = Relationship(back_populates="user")
```

### Task Model
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: Optional[str] = None
    status: str = "Pending"
    priority: str = "Medium"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    user: User = Relationship(back_populates="tasks")
```

---

## Key Features to Implement

### 1. Connection Management
- Initialize connection pool on startup
- Configure pool size and timeout
- Handle connection lifecycle
- Implement connection health checks
- Graceful shutdown

### 2. Session Management
- Create session factory with proper settings
- Implement async session context managers
- Handle transaction management
- Implement session cleanup
- Support nested transactions

### 3. Index Strategy
- User ID index for filtering
- Status index for filtering
- Composite indexes for common queries
- Timestamp indexes for sorting
- Regular index analysis

### 4. Query Patterns
- SELECT with filtering and pagination
- JOINs for user + task queries
- Aggregate functions (COUNT, SUM)
- Batch operations for performance
- Query result caching

### 5. Data Validation
- Column type constraints
- Unique constraints (email)
- Foreign key constraints
- Check constraints (status enum)
- Length constraints

### 6. Migration Strategy
- Initial schema migration
- Versioned migrations
- Rollback capabilities
- Data migration scripts
- Schema documentation

### 7. Performance
- Connection pooling optimization
- Index usage analysis
- Query execution plans
- Slow query logging
- Batch insert optimization

### 8. Backup & Recovery
- Backup strategies
- Point-in-time recovery
- Data archival
- Cleanup of soft-deleted data
- Disaster recovery procedures

---

## Migration Workflow

### Creating a Migration
```bash
alembic revision --autogenerate -m "add new column"
alembic upgrade head  # Apply migration
alembic downgrade -1  # Rollback migration
```

### Migration File Structure
```python
"""Add new column

Revision ID: xyz123
Revises: abc123
Create Date: 2025-12-14
"""

def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.String(20), server_default='Medium'))

def downgrade():
    op.drop_column('tasks', 'priority')
```

---

## Testing Requirements

### Unit Tests
- Model field validation
- Constraint enforcement
- Relationship definitions
- Default values
- Field types

### Integration Tests
- CRUD operations
- Transaction behavior
- Cascade deletes
- Index usage
- Query performance

### Migration Tests
- Upgrade/downgrade cycles
- Data preservation
- Schema consistency
- Rollback scenarios
- Empty database handling

### Performance Tests
- Query execution time
- Index effectiveness
- Connection pool efficiency
- Bulk operations
- Memory usage

### Data Integrity Tests
- Foreign key constraints
- Unique constraints
- NOT NULL constraints
- Check constraints
- Referential integrity

---

## Performance Targets

| Metric | Target |
|--------|--------|
| **Connection Pool Response** | < 10ms |
| **Single Row Query** | < 50ms |
| **List Query (100 rows)** | < 100ms |
| **Index Scan** | < 50ms |
| **Insert Operation** | < 20ms |
| **Update Operation** | < 20ms |
| **Delete Operation** | < 20ms |
| **Concurrent Connections** | 1,000+ |
| **Query Result Caching** | 95%+ hit rate |

---

## Configuration

### Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
DATABASE_ECHO=false
SQLALCHEMY_WARN_20=true
```

### Connection String Format
```
postgresql://user:password@host:port/database
postgresql+asyncpg://user:password@host:port/database
```

---

## Acceptance Criteria

- [ ] All tables created with proper schema
- [ ] Foreign key relationships defined
- [ ] Indexes created for performance
- [ ] Constraints properly configured
- [ ] Migrations working (upgrade/downgrade)
- [ ] SQLModel definitions complete
- [ ] Connection pooling configured
- [ ] Session management implemented
- [ ] All tests passing (≥80% coverage)
- [ ] Query performance meets targets
- [ ] Data integrity verified
- [ ] Documentation complete

---

## Related Specifications

- `@specs/features/task-crud-web.md` - Task requirements
- `@specs/features/authentication.md` - User requirements
- `@specs/api/rest-endpoints.md` - API contracts
- `@specs/agents/backend-agent.md` - Backend integration

---

**Agent Status**: 🔄 Ready for Implementation

**Next Step**: Follow `database-skills.md` for detailed capabilities
