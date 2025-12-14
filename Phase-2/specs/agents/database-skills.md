# Database Agent Skills

**Agent Name**: Database Agent (PostgreSQL Specialist)
**Domain**: Database - Data Persistence & Schema Management
**Total Skills**: 10 Core + 7 Advanced

---

## Core Skills (Essential for Phase-2)

### 1. Schema Design & Normalization

**Purpose**: Design normalized database schemas following best practices

**Example Query**: "Design schema for users and tasks with proper relationships"

**Expected Action**:
- Create normalized tables (3rd NF)
- Define primary/foreign keys
- Implement relationships
- Avoid redundancy
- Document schema

**Technical Skills**:
- Database normalization
- Table design
- Key constraints
- Relationships (1:1, 1:N, M:N)
- Schema documentation

---

### 2. Table Creation & Constraints

**Purpose**: Create tables with appropriate constraints and validations

**Example Query**: "Create users table with email uniqueness constraint"

**Expected Action**:
- Create table with columns
- Define primary keys
- Add UNIQUE constraints
- Add NOT NULL constraints
- Add CHECK constraints

**Technical Skills**:
- CREATE TABLE syntax
- Data types (VARCHAR, INT, TIMESTAMP, etc.)
- Constraints (PRIMARY KEY, UNIQUE, NOT NULL, CHECK)
- DEFAULT values
- Column constraints

---

### 3. Indexes & Query Optimization

**Purpose**: Create indexes to improve query performance

**Example Query**: "Create index on user_id for faster task filtering"

**Expected Action**:
- Identify slow queries
- Create appropriate indexes
- Use EXPLAIN ANALYZE
- Optimize composite indexes
- Monitor index usage

**Technical Skills**:
- INDEX creation
- EXPLAIN ANALYZE
- Query plans
- Composite indexes
- Index statistics

---

### 4. Foreign Keys & Relationships

**Purpose**: Enforce data integrity through foreign key relationships

**Example Query**: "Create foreign key from tasks to users table"

**Expected Action**:
- Define foreign keys
- Set referential actions (CASCADE, SET NULL)
- Ensure referential integrity
- Handle cascading deletes
- Test relationships

**Technical Skills**:
- FOREIGN KEY syntax
- Referential actions
- Cascade operations
- Constraint checking
- Relationship testing

---

### 5. SQLModel ORM Mapping

**Purpose**: Map database tables to Python SQLModel classes

**Example Query**: "Create SQLModel for Task with relationships"

**Expected Action**:
- Define SQLModel class
- Map table structure
- Define relationships
- Add field validation
- Configure ORM options

**Technical Skills**:
- SQLModel syntax
- Field mapping
- Relationships
- Validators
- ORM configuration

---

### 6. Query Building with SQLAlchemy

**Purpose**: Build efficient queries using SQLAlchemy ORM

**Example Query**: "Query tasks filtered by user_id with pagination"

**Expected Action**:
- Write SQL queries using ORM
- Use filter() for WHERE clause
- Implement pagination (limit/offset)
- Use join() for relationships
- Optimize query performance

**Technical Skills**:
- SQLAlchemy query API
- filter() clauses
- JOIN operations
- Pagination
- Query optimization

---

### 7. Session & Connection Management

**Purpose**: Manage database connections and sessions properly

**Example Query**: "Create session factory for database operations"

**Expected Action**:
- Create SQLAlchemy engine
- Configure connection pooling
- Create session factory
- Implement session lifecycle
- Handle cleanup

**Technical Skills**:
- create_engine()
- Session factory
- Connection pooling
- Session lifecycle
- Resource cleanup

---

### 8. Data Migration with Alembic

**Purpose**: Create and manage database migrations for schema evolution

**Example Query**: "Create migration to add priority column to tasks"

**Expected Action**:
- Initialize Alembic
- Create migration scripts
- Apply migrations
- Rollback migrations
- Version control

**Technical Skills**:
- Alembic commands
- Migration scripts
- upgrade/downgrade functions
- Autogenerate migrations
- Version management

---

### 9. Transaction Management

**Purpose**: Ensure data consistency with proper transaction handling

**Example Query**: "Use transaction to ensure task creation succeeds or fails atomically"

**Expected Action**:
- Use transactions for multi-step operations
- Implement ACID properties
- Handle rollbacks
- Use commit/rollback
- Test transaction behavior

**Technical Skills**:
- Transaction control
- COMMIT/ROLLBACK
- ACID properties
- Isolation levels
- Error recovery

---

### 10. Database Testing & Validation

**Purpose**: Test database operations and validate data integrity

**Example Query**: "Test that cascade delete removes all user's tasks"

**Expected Action**:
- Write database tests
- Test constraints
- Test relationships
- Test migrations
- Verify data integrity

**Technical Skills**:
- pytest database fixtures
- Test transactions
- Seed test data
- Assertion validation
- Data integrity testing

---

## Advanced Skills (Optional for Phase-2)

### 11. Query Performance Tuning

**Purpose**: Analyze and optimize slow queries

**Example Query**: "Optimize slow task list query"

**Technical Skills**: EXPLAIN ANALYZE, execution plans, index optimization, query refactoring

---

### 12. Backup & Recovery Strategies

**Purpose**: Implement backup and disaster recovery

**Example Query**: "Configure daily backups"

**Technical Skills**: PostgreSQL backup tools, point-in-time recovery, backup verification

---

### 13. Connection Pooling Optimization

**Purpose**: Configure optimal connection pool settings

**Example Query**: "Set pool size to 20 with max overflow of 10"

**Technical Skills**: Pool configuration, sizing, monitoring, connection reuse

---

### 14. Partitioning & Sharding

**Purpose**: Handle large datasets with partitioning

**Example Query**: "Partition tasks table by user_id"

**Technical Skills**: Table partitioning, sharding strategies, partition management

---

### 15. Data Archival & Cleanup

**Purpose**: Manage old data and maintain performance

**Example Query**: "Archive completed tasks older than 1 year"

**Technical Skills**: Data archival, soft deletes, cleanup jobs, retention policies

---

### 16. Audit & Logging

**Purpose**: Track data changes for compliance and debugging

**Example Query**: "Log all changes to task status"

**Technical Skills**: Audit tables, change tracking, audit trails, timestamps

---

### 17. Multi-Tenancy Support

**Purpose**: Support multiple isolated tenants in same database

**Example Query**: "Partition data per tenant with isolation"

**Technical Skills**: Tenant isolation, row-level security, data filtering

---

## Skill Composition Example

### Database Setup Workflow
```
1. Design schema (Skill #1: Schema Design)
2. Create tables (Skill #2: Table Creation)
3. Add constraints (Skill #2: Constraints)
4. Create foreign keys (Skill #4: Foreign Keys)
5. Create indexes (Skill #3: Indexes)
6. Map to SQLModel (Skill #5: SQLModel)
7. Configure connections (Skill #7: Session Management)
8. Create migrations (Skill #8: Alembic)
9. Test database (Skill #10: Testing)
```

---

## Skill Dependencies

```
Schema Design (#1)
    ├─ Table Creation (#2)
    ├─ Foreign Keys (#4)
    ├─ SQLModel Mapping (#5)
    └─ Documentation

Table Creation (#2)
    ├─ Indexes (#3)
    ├─ Foreign Keys (#4)
    ├─ Constraints
    └─ Testing (#10)

Indexes (#3)
    ├─ Query Building (#6)
    ├─ Performance Tuning (#11)
    └─ Testing (#10)

Foreign Keys (#4)
    ├─ Relationships (#5 SQLModel)
    ├─ Transactions (#9)
    └─ Cascade Operations

Query Building (#6)
    ├─ SQLModel Mapping (#5)
    ├─ Indexes (#3)
    ├─ Pagination
    └─ Testing (#10)

Session Management (#7)
    ├─ Connection pooling (#13 advanced)
    ├─ Transaction Management (#9)
    └─ Error Handling

Migrations (#8)
    ├─ Schema Changes
    ├─ Version Control
    ├─ Rollback Strategy
    └─ Testing (#10)
```

---

## Guardrails

### Must Do
- ✅ Normalize schema (3rd NF minimum)
- ✅ Add constraints for data integrity
- ✅ Create indexes for performance
- ✅ Use ORM for SQL safety
- ✅ Test all database operations
- ✅ Implement migrations for changes
- ✅ Document schema

### Must Not Do
- ❌ Use raw SQL queries (use ORM)
- ❌ Skip constraint enforcement
- ❌ Create N+1 query problems
- ❌ Leave unused indexes
- ❌ Modify production without migration
- ❌ Store sensitive data unencrypted
- ❌ Skip backup procedures

### Out of Scope
- NoSQL databases (Phase-3+)
- Complex sharding (Phase-5+)
- Advanced replication
- Graph databases
- Document databases
- Column stores

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Query Response Time** | < 100ms (p95) |
| **Connection Pool Efficiency** | > 95% |
| **Index Coverage** | All common queries indexed |
| **Data Integrity** | 100% constraint compliance |
| **Migration Success Rate** | 100% |
| **Test Coverage** | ≥ 80% |
| **Backup Frequency** | Daily |

---

## Configuration Reference

### PostgreSQL Connection URL
```
postgresql://username:password@localhost:5432/dbname
```

### SQLAlchemy Engine Setup
```python
from sqlalchemy import create_engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30
)
```

### Session Factory
```python
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

**Skill Status**: Ready for use by Database Agent

**Related**: database-agent.md, database-agent tasks
