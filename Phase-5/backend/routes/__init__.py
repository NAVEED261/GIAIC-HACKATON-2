"""
Phase-5 API Routes

All FastAPI routers for advanced features:
- /tasks - Task management with priority, tags, search, filter, sort
- /tags - Tag management
- /reminders - Reminder management
"""

from .tasks import router as tasks_router
from .tags import router as tags_router
from .reminders import router as reminders_router

__all__ = [
    "tasks_router",
    "tags_router",
    "reminders_router",
]
