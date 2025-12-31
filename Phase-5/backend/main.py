"""
Phase-5 Backend - Main Entry Point
FastAPI application with advanced features

@author: Phase-5 System
@specs: Phase-5/specs/spec.md
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from db import init_db, get_session, engine
from models import User, UserCreate, UserRead, UserLogin
from models.user import ReminderPreferences
from middleware.auth import create_access_token, get_current_user
from routes import tasks_router, tags_router, reminders_router, chat_router, conversations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    # Startup
    print("[*] Starting Phase-5 Backend...")
    init_db()
    print("[OK] Database initialized")
    yield
    # Shutdown
    print("[*] Shutting down Phase-5 Backend...")


# Create FastAPI app
app = FastAPI(
    title="Phase-5 Todo API",
    description="Advanced Todo API with recurring tasks, reminders, priorities, and tags",
    version="5.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router, prefix="/api")
app.include_router(tags_router, prefix="/api")
app.include_router(reminders_router, prefix="/api")
app.include_router(chat_router)  # Already has /api/chat prefix
app.include_router(conversations_router)  # Already has /api/conversations prefix


# ==================== Health & Info ====================

@app.get("/health")
async def health_check():
    """Health check endpoint for K8s probes"""
    return {"status": "healthy", "phase": 5}


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Phase-5 Todo API",
        "version": "5.0.0",
        "features": [
            "Recurring Tasks",
            "Due Dates & Reminders",
            "Task Priorities",
            "Tags & Categories",
            "Search, Filter, Sort"
        ],
        "docs": "/docs",
        "health": "/health"
    }


# ==================== Auth Endpoints ====================

@app.post("/api/auth/register", response_model=UserRead, status_code=201)
async def register(user_data: UserCreate):
    """Register a new user"""
    with Session(engine) as session:
        # Check if email exists
        existing = session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create user
        user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=User.hash_password(user_data.password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


@app.post("/api/auth/login")
async def login(credentials: UserLogin):
    """Login and get JWT token"""
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == credentials.email)
        ).first()

        if not user or not user.verify_password(credentials.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create token
        token = create_access_token({"sub": str(user.id)})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }


@app.get("/api/auth/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """Get current user info - requires auth"""
    return current_user


# ==================== Dapr Endpoints ====================

@app.get("/dapr/subscribe")
async def dapr_subscribe():
    """Dapr subscription configuration - Dapr calls this on startup"""
    return [
        {
            "pubsubname": "pubsub",
            "topic": "task-events",
            "route": "/api/events/tasks"
        },
        {
            "pubsubname": "pubsub",
            "topic": "reminders",
            "route": "/api/events/reminders"
        }
    ]


@app.post("/api/events/tasks")
async def handle_task_events(event: dict):
    """Handle task events from Kafka"""
    import logging
    logging.info(f"Task event received: {event}")
    return {"status": "ok"}


@app.post("/api/events/reminders")
async def handle_reminder_events(event: dict):
    """Handle reminder events from Kafka"""
    import logging
    logging.info(f"Reminder event received: {event}")
    return {"status": "ok"}


# ==================== Run Server ====================

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )
