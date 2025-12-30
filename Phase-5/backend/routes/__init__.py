"""
Phase-5 API Routes

All FastAPI routers for advanced features:
- /tasks - Task management with priority, tags, search, filter, sort
- /tags - Tag management
- /reminders - Reminder management
- /chat - AI Chat with OpenAI
- /conversations - Chat history management
"""

from .tasks import router as tasks_router
from .tags import router as tags_router
from .reminders import router as reminders_router
from .chat import router as chat_router
from .conversations import router as conversations_router

__all__ = [
    "tasks_router",
    "tags_router",
    "reminders_router",
    "chat_router",
    "conversations_router",
]
