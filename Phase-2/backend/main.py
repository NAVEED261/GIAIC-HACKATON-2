"""
FastAPI Application Main Entry Point
Phase-2: Backend Agent
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import create_all_tables, engine


# Create FastAPI app
app = FastAPI(
    title="Hackathon-2 Task Management API",
    description="Full-stack task management system - Phase-2",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on application startup"""
    create_all_tables(engine)


# Health Check Endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "task-management-api",
        "version": "2.0.0"
    }


@app.get("/health/db", tags=["Health"])
async def health_check_db():
    """Database health check endpoint"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return {
            "status": "connected",
            "database": "ok",
            "service": "task-management-api"
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "database": "error",
            "error": str(e)
        }, 503


# TODO: Import and include routers
# from routes import tasks_router, auth_router
# app.include_router(tasks_router)
# app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
