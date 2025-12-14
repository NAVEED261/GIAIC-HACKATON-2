"""
Database Connection Setup
Phase-2: Database Agent
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel


def get_database_url() -> str:
    """
    Get database URL from environment variables or use default SQLite for development.

    Returns:
        Database connection URL string

    Environment Variables:
        DATABASE_URL: PostgreSQL connection string
        If not set, uses SQLite for development
    """
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db"  # Default SQLite for development
    )
    return database_url


def create_db_engine():
    """
    Create SQLAlchemy engine with appropriate configuration.

    Returns:
        SQLAlchemy engine instance
    """
    database_url = get_database_url()

    # Use different configuration based on database type
    if database_url.startswith("sqlite"):
        # SQLite configuration (for development/testing)
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
    else:
        # PostgreSQL configuration (for production)
        engine = create_engine(
            database_url,
            pool_size=int(os.getenv("DATABASE_POOL_SIZE", "20")),
            max_overflow=int(os.getenv("DATABASE_MAX_OVERFLOW", "10")),
            pool_timeout=int(os.getenv("DATABASE_POOL_TIMEOUT", "30")),
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )

    return engine


def create_all_tables(engine):
    """
    Create all database tables from SQLModel definitions.

    Args:
        engine: SQLAlchemy engine instance
    """
    SQLModel.metadata.create_all(engine)


# Create engine instance (will be used by session factory)
engine = create_db_engine()
