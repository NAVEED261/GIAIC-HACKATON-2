"""
API Routes Package

Exports all route routers for inclusion in FastAPI app.
"""

from .auth import router as auth_router
from .tasks import router as tasks_router
from .health import router as health_router

__all__ = [
    "auth_router",
    "tasks_router",
    "health_router",
]
