"""
Database Configuration - Phase-5
PostgreSQL connection with SQLModel

@author: Phase-5 System
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

# Load .env file
load_dotenv()
from typing import Generator

# Database URL from environment or default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./phase5_test.db"  # Default to SQLite for local testing
)

# For SQLite testing
SQLITE_URL = "sqlite:///./phase5_test.db"

# Check if using SQLite or PostgreSQL
is_sqlite = DATABASE_URL.startswith("sqlite")

if is_sqlite:
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session (dependency injection)"""
    with Session(engine) as session:
        yield session


# For Dapr state store integration
class DaprStateStore:
    """Dapr state store wrapper for caching"""

    def __init__(self, dapr_port: int = 3500, store_name: str = "statestore"):
        self.dapr_url = f"http://localhost:{dapr_port}"
        self.store_name = store_name

    async def save_state(self, key: str, value: dict):
        """Save state to Dapr store"""
        import httpx
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.dapr_url}/v1.0/state/{self.store_name}",
                json=[{"key": key, "value": value}]
            )

    async def get_state(self, key: str) -> dict:
        """Get state from Dapr store"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.dapr_url}/v1.0/state/{self.store_name}/{key}"
            )
            if response.status_code == 200:
                return response.json()
            return None

    async def delete_state(self, key: str):
        """Delete state from Dapr store"""
        import httpx
        async with httpx.AsyncClient() as client:
            await client.delete(
                f"{self.dapr_url}/v1.0/state/{self.store_name}/{key}"
            )
