"""
FastAPI Application Main Entry Point
Phase-2: Backend Agent

This module initializes the FastAPI application with:
- CORS middleware for cross-origin requests
- Database initialization on startup
- Route registration (auth, tasks, health)
- Comprehensive error handling
- OpenAPI/Swagger documentation

The application is organized following these principles:
1. Models: SQLModel definitions (models/*)
2. Database: Connection and session management (db/*)
3. Routes: Endpoint handlers organized by domain (routes/*)
4. Dependencies: Reusable functions (dependencies/*, db/*)
5. Utilities: Helpers and middleware (if needed)
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from db import create_all_tables, engine
from routes import auth_router, tasks_router, health_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Create FastAPI app with comprehensive documentation
app = FastAPI(
    title="Hackathon-2 Task Management API",
    description="""
    A production-ready REST API for task management with:
    - User authentication (JWT tokens)
    - Multi-user support with complete data isolation
    - Task CRUD operations
    - Pagination and filtering
    - Comprehensive error handling
    - OpenAPI/Swagger documentation

    **Base URL:** /api
    **Health Checks:** /health, /health/db
    **Documentation:** /docs (Swagger), /redoc (ReDoc)
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Development Team",
        "url": "https://github.com/NAVEED261/GIAIC-HACKATON-2",
    },
    license_info={
        "name": "MIT",
    },
)

# ============================================================================
# Middleware Configuration
# ============================================================================

# Configure CORS - Allow cross-origin requests from frontend
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
origins = [origin.strip() for origin in origins]  # Clean whitespace

logger.info(f"CORS enabled for origins: {origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add trusted host middleware for security (optional, can be configured)
# Uncomment to enable strict host checking
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["localhost", "127.0.0.1"]
# )


# ============================================================================
# Event Handlers
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Application startup event.

    Runs once when application starts. Creates database tables if they
    don't exist. Uses SQLModel to initialize schema from models.
    """
    logger.info("Starting application initialization...")
    try:
        create_all_tables(engine)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.

    Runs when application is shutting down. Performs cleanup tasks
    like closing connections, flushing logs, etc.
    """
    logger.info("Application shutting down...")
    # TODO: Add cleanup logic here (close connections, flush logs, etc.)


# ============================================================================
# Route Registration
# ============================================================================

# Register health check routes
# These don't require authentication
app.include_router(health_router)

# Register authentication routes
# POST /api/auth/signup, /api/auth/login, /api/auth/logout, etc.
app.include_router(auth_router)

# Register task management routes
# GET/POST /api/tasks, PUT/DELETE /api/tasks/{id}, etc.
app.include_router(tasks_router)

logger.info("All route routers registered successfully")


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint providing API information.

    Returns:
        dict: API information and links to documentation
    """
    return {
        "message": "Hackathon-2 Task Management API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/health",
        "health_db": "/health/db",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
