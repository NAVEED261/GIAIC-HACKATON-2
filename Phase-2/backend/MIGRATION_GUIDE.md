# Migration Management Guide

## Quick Reference

### Setup (First Time)
```bash
cd Phase-2/backend
# Create .env with DATABASE_URL
# Install dependencies
pip install -r requirements.txt
# Run migrations
alembic upgrade head
```

### Development Workflow

#### Check current schema version
```bash
alembic current
```

#### View all migrations
```bash
alembic history
```

#### Make a schema change
1. Modify model in `models/` (user.py or task.py)
2. Create migration:
   ```bash
   alembic revision --autogenerate -m "Add new column"
   ```
3. Review generated migration in `alembic/versions/`
4. Apply migration:
   ```bash
   alembic upgrade head
   ```

#### Undo last migration
```bash
alembic downgrade -1
```

#### Revert to specific version
```bash
alembic downgrade 001  # Go back to initial migration
```

## File Structure

```
backend/
├── alembic/
│   ├── versions/              # All migration files
│   │   └── 0001_initial_migration.py
│   ├── env.py                 # Alembic environment config
│   ├── README                 # Alembic README
│   ├── script.py.mako         # Migration template
│   └── MIGRATIONS.md          # Migration documentation
├── alembic.ini                # Alembic configuration
├── MIGRATION_GUIDE.md         # This file
├── models/                    # SQLModel definitions
├── db/                        # Database connection/session
├── requirements.txt           # Production dependencies
└── requirements-dev.txt       # Development dependencies (SQLite)
```

## Key Points

### Database URL Format
- **SQLite (development):** `sqlite:///./test.db`
- **PostgreSQL (production):** `postgresql://user:password@host:5432/dbname`

### Migration Naming Convention
- Format: `NNNN_description.py`
- Example: `0001_initial_migration.py`, `0002_add_task_priority.py`
- Revision IDs: Simple increment (001, 002, 003, etc.)

### Index Strategy
All indexes in migration 0001 serve documented query patterns:

| Index | Query Pattern | Performance |
|-------|---------------|-------------|
| `ix_user_email` | Login by email | O(1) exact match |
| `ix_task_user_id` | Load user's tasks | Avoid full table scan |
| `ix_task_status` | Filter by status | Group by status (Kanban) |
| `ix_task_title` | Search tasks | Full-text or prefix search |
| `ix_task_created_at` | Sort by date | ORDER BY without scan |
| `ix_task_user_status` | User + status combo | Most common dashboard query |

### Foreign Key Constraints
- `task.user_id → user.id` with CASCADE DELETE
- When user deleted, all tasks automatically removed
- Prevents orphaned tasks

## Troubleshooting

### Issue: "Column already exists"
**Cause:** Running migration twice
**Solution:** Check `alembic_version` table - migration may have already run

### Issue: "Can't connect to database"
**Cause:** DATABASE_URL not set or invalid
**Solution:** Check `.env` file, ensure database server is running

### Issue: "Alembic can't find models"
**Cause:** Import path issue
**Solution:** Ensure models/ has `__init__.py` and environment is set up correctly

### Issue: "Permission denied creating test.db"
**Cause:** Directory permissions
**Solution:** Run from backend/ directory or ensure write permissions

## Integration with FastAPI

The migration system is separate from the FastAPI startup event. Both should work together:

1. **On app startup:** `main.py` calls `create_all_tables(engine)` to create any missing tables
2. **For production:** Run `alembic upgrade head` before deploying
3. **For development:** SQLite test.db is auto-created on first run

## Best Practices

✅ **DO:**
- Create migrations for ALL schema changes
- Test migrations both upgrade and downgrade
- Write descriptive migration messages
- Document complex index decisions
- Keep migrations small and focused

❌ **DON'T:**
- Manually edit database without migrations
- Modify production database directly
- Skip downgrade() function
- Create migrations without testing
- Use raw SQL without proper formatting

## Next Steps

Phase 2B migrations will likely include:
- Task history/audit log table
- Task tags and categories (many-to-many)
- Notification settings
- Additional user profile fields
- Performance metrics tracking

Each new phase should follow this same process:
1. Add new models
2. Create Alembic migrations
3. Test upgrade/downgrade
4. Document indexes and foreign keys
5. Update this guide
