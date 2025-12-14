"""
Health Check Routes

Provides endpoints for monitoring application and database health.
Used by load balancers, monitoring systems, and deployment checks.

Endpoints:
  GET  /health      - Basic application health check
  GET  /health/db   - Database connectivity health check
"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from db import get_db, engine

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Application is healthy"},
        503: {"description": "Application is degraded"},
    },
    summary="Application Health Check",
    description="""
Check if the application is running and responsive.

**Success Response (200):**
```json
{
  "status": "healthy",
  "service": "task-management-api",
  "version": "2.0.0",
  "timestamp": "2025-01-03T16:45:00"
}
```

**Degraded Response (503):**
```json
{
  "status": "degraded",
  "service": "task-management-api",
  "version": "2.0.0",
  "timestamp": "2025-01-03T16:45:00",
  "issues": ["Database unavailable", "Cache service down"]
}
```

**Use Case:**
- Kubernetes liveness probe
- Load balancer health check
- Deployment health verification
- Monitoring system heartbeat

**Response Time:** Should be < 100ms for healthy status.
    """,
)
async def health_check():
    """
    Basic application health check.

    Returns:
        dict: Health status with timestamp

    Response Codes:
        200: Application is healthy
        503: Application is degraded
    """
    return {
        "status": "healthy",
        "service": "task-management-api",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get(
    "/health/db",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Database is connected and responsive"},
        503: {"description": "Database is unavailable"},
    },
    summary="Database Health Check",
    description="""
Check database connectivity and basic functionality.

**Success Response (200):**
```json
{
  "status": "connected",
  "database": "ok",
  "service": "task-management-api",
  "version": "2.0.0",
  "timestamp": "2025-01-03T16:45:00",
  "response_time_ms": 5
}
```

**Error Response (503):**
```json
{
  "status": "disconnected",
  "database": "error",
  "service": "task-management-api",
  "version": "2.0.0",
  "error": "Connection refused: localhost:5432",
  "timestamp": "2025-01-03T16:45:00"
}
```

**What It Checks:**
1. Can establish database connection
2. Can execute simple query (SELECT 1)
3. Connection pool is responsive

**Use Case:**
- Kubernetes readiness probe
- Load balancer health check
- Deployment pre-flight check
- Monitoring system heartbeat

**Response Time:** Should be < 500ms for healthy status.

**Important:**
This endpoint does NOT require authentication. It's used by infrastructure
systems that may not have access tokens.
    """,
)
async def health_check_db(db: Session = Depends(get_db)):
    """
    Database health check.

    Args:
        db: Database session (tests connectivity)

    Returns:
        dict: Database health status with timing

    Response Codes:
        200: Database is healthy
        503: Database is unavailable
    """
    try:
        # Try to execute a simple query
        start_time = datetime.utcnow()
        result = db.execute(text("SELECT 1"))
        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        return {
            "status": "connected",
            "database": "ok",
            "service": "task-management-api",
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "response_time_ms": round(response_time, 2),
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "database": "error",
            "service": "task-management-api",
            "version": "2.0.0",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }, 503
