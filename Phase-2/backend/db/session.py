"""
Database Session Management
Phase-2: Database Agent
"""

from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from .connection import engine


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI routes to get database session.

    Yields:
        Database session

    Usage in FastAPI:
        @app.get("/api/tasks")
        def list_tasks(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
