# Part A: Advanced Features Specification

## Overview

**Part**: A (Advanced Features)
**Type**: Code Implementation
**Card Required**: NO (100% FREE)
**Dependencies**: Phase-3 Backend + Frontend

---

## Feature 1: Recurring Tasks

### User Stories
- As a user, I can create a recurring task that auto-creates next occurrence
- As a user, I can set recurrence patterns (daily, weekly, monthly)
- As a user, I can stop a recurring task series

### Recurrence Patterns

| Pattern | Example | Description |
|---------|---------|-------------|
| daily | Every day | Task repeats daily |
| weekly | Every Monday | Task repeats weekly on same day |
| monthly | Every 15th | Task repeats monthly on same date |
| custom | Every 3 days | Custom interval |

### Database Fields

```python
is_recurring: bool = False
recurrence_pattern: str  # daily, weekly, monthly, custom
recurrence_interval: int  # every N units
next_occurrence: datetime
parent_task_id: int  # links to original recurring task
```

### MCP Tool: create_recurring_task

```python
@tool
async def create_recurring_task(
    user_id: str,
    title: str,
    pattern: str,  # daily, weekly, monthly, custom
    interval: int = 1,
    description: str = None
) -> dict:
    """Create a recurring task"""
```

### Kafka Event

```json
{
  "event_type": "recurring_task_completed",
  "task_id": 1,
  "pattern": "weekly",
  "next_occurrence": "2026-01-25T09:00:00Z"
}
```

---

## Feature 2: Due Dates & Reminders

### User Stories
- As a user, I can set a due date for a task
- As a user, I can set a reminder before the due date
- As a user, I receive notification when reminder triggers

### Reminder Options

| Option | Description |
|--------|-------------|
| At due time | Notify exactly at due date/time |
| 1 hour before | Notify 1 hour before |
| 1 day before | Notify 24 hours before |
| Custom | User-specified time |

### Database Fields

```python
due_date: datetime
reminder_at: datetime
reminder_sent: bool = False
```

### MCP Tools

```python
@tool
async def set_due_date(user_id: str, task_id: int, due_date: str) -> dict:
    """Set due date for a task"""

@tool
async def set_reminder(user_id: str, task_id: int, remind_at: str) -> dict:
    """Set reminder for a task"""
```

### Kafka Event

```json
{
  "event_type": "reminder_due",
  "task_id": 1,
  "title": "Complete report",
  "remind_at": "2026-01-18T08:00:00Z",
  "user_id": "user123"
}
```

---

## Feature 3: Priorities

### User Stories
- As a user, I can set priority (high, medium, low)
- As a user, I can see visual priority indicators
- As a user, I can sort tasks by priority

### Priority Levels

| Level | Color | Emoji | Sort Order |
|-------|-------|-------|------------|
| high | Red | 🔴 | 1 (top) |
| medium | Yellow | 🟡 | 2 |
| low | Green | 🟢 | 3 (bottom) |

### Database Field

```python
priority: str = "medium"  # high, medium, low
```

### MCP Tool

```python
@tool
async def set_priority(user_id: str, task_id: int, priority: str) -> dict:
    """Set task priority: high, medium, low"""
```

---

## Feature 4: Tags/Categories

### User Stories
- As a user, I can add tags to a task
- As a user, I can filter tasks by tag
- As a user, I can create custom tags

### Default Tags

| Tag | Color | Description |
|-----|-------|-------------|
| work | Blue | Work-related tasks |
| home | Green | Home/personal tasks |
| urgent | Red | Urgent tasks |
| shopping | Purple | Shopping list items |

### Database Fields

```python
# Task model
tags: List[str] = []

# Tag model (new table)
class Tag(SQLModel, table=True):
    id: int
    name: str
    user_id: str
    color: str
```

### MCP Tools

```python
@tool
async def add_tags(user_id: str, task_id: int, tags: List[str]) -> dict:
    """Add tags to a task"""

@tool
async def remove_tags(user_id: str, task_id: int, tags: List[str]) -> dict:
    """Remove tags from a task"""

@tool
async def list_tags(user_id: str) -> dict:
    """List all user's tags"""
```

---

## Feature 5: Search

### User Stories
- As a user, I can search tasks by keyword
- As a user, I can search in title and description
- As a user, I get instant search results

### Search Implementation

```python
# SQL Query
SELECT * FROM tasks
WHERE user_id = :user_id
AND (
    title ILIKE '%keyword%'
    OR description ILIKE '%keyword%'
)
```

### MCP Tool

```python
@tool
async def search_tasks(user_id: str, query: str) -> dict:
    """Search tasks by keyword in title or description"""
```

### API Endpoint

```
GET /api/{user_id}/tasks/search?q=meeting
```

---

## Feature 6: Filter

### User Stories
- As a user, I can filter by status (pending, completed, all)
- As a user, I can filter by priority
- As a user, I can filter by tags
- As a user, I can filter by date range
- As a user, I can combine multiple filters

### Filter Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| status | all, pending, completed | Task completion status |
| priority | high, medium, low | Priority level |
| tags | work, home, urgent, ... | Tag names (comma-separated) |
| due_from | ISO date | Due date start range |
| due_to | ISO date | Due date end range |

### MCP Tool

```python
@tool
async def filter_tasks(
    user_id: str,
    status: str = "all",
    priority: str = None,
    tags: List[str] = None,
    due_from: str = None,
    due_to: str = None
) -> dict:
    """Filter tasks by multiple criteria"""
```

### API Endpoint

```
GET /api/{user_id}/tasks?status=pending&priority=high&tags=work,urgent
```

---

## Feature 7: Sort

### User Stories
- As a user, I can sort by due date
- As a user, I can sort by priority
- As a user, I can sort alphabetically
- As a user, I can sort by created date
- As a user, I can choose ascending/descending

### Sort Options

| Sort By | Order | Description |
|---------|-------|-------------|
| due_date | asc/desc | Sort by due date |
| priority | asc/desc | Sort by priority level |
| title | asc/desc | Sort alphabetically |
| created_at | asc/desc | Sort by creation date |
| updated_at | asc/desc | Sort by last update |

### MCP Tool

```python
@tool
async def sort_tasks(
    user_id: str,
    sort_by: str = "created_at",
    order: str = "desc"
) -> dict:
    """Sort tasks by specified field"""
```

### API Endpoint

```
GET /api/{user_id}/tasks?sort=due_date&order=asc
```

---

## Combined Query Example

### Natural Language
> "Show me high priority work tasks due this week sorted by due date"

### AI Parses To
```python
filter_tasks(
    user_id="user123",
    status="pending",
    priority="high",
    tags=["work"],
    due_from="2026-01-18",
    due_to="2026-01-25"
)
# Then sort by due_date ascending
```

### API Call
```
GET /api/user123/tasks?status=pending&priority=high&tags=work&due_from=2026-01-18&due_to=2026-01-25&sort=due_date&order=asc
```

---

## Implementation Checklist

### Backend
- [ ] Update Task model with new fields
- [ ] Create Reminder model
- [ ] Create Tag model
- [ ] Add new MCP tools (9 tools)
- [ ] Update existing task CRUD routes
- [ ] Add search endpoint
- [ ] Add filter logic
- [ ] Add sort logic
- [ ] Add recurring task logic
- [ ] Add reminder scheduling logic

### Frontend
- [ ] Priority selector component
- [ ] Tags input component
- [ ] Date/time picker for due dates
- [ ] Reminder selector
- [ ] Search bar
- [ ] Filter panel
- [ ] Sort dropdown
- [ ] Recurring task options

### Database
- [ ] Migrate Task table with new columns
- [ ] Create Reminder table
- [ ] Create Tag table
- [ ] Add indexes for search/filter performance

---

*Part A Specification Version: 1.0*
*Created: 2025-12-28*
