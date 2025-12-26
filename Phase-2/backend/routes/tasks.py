"""
Task Management Routes

Handles CRUD operations for tasks: create, read, update, delete, complete.
All operations are scoped to authenticated user (multi-user isolation).
All endpoints include OpenAPI documentation and error handling.

Endpoints:
  GET    /api/tasks              - List user's tasks (paginated)
  POST   /api/tasks              - Create new task
  GET    /api/tasks/{id}         - Get task details
  PUT    /api/tasks/{id}         - Update task
  DELETE /api/tasks/{id}         - Delete task
  PATCH  /api/tasks/{id}/complete - Mark task complete
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, validator

from db import get_db
from models.task import Task, TaskResponse, TaskCreate, TaskUpdate
from models.user import User
from dependencies.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


# ============================================================================
# Request/Response Schema Classes
# ============================================================================

class TaskListQuery(BaseModel):
    """Query parameters for task list endpoint."""
    skip: int = Query(0, ge=0, description="Number of tasks to skip")
    limit: int = Query(10, ge=1, le=100, description="Number per page (max 100)")
    status: Optional[str] = Query(None, description="Filter by status")
    sort_by: str = Query("created_at", description="Sort field")
    order: str = Query("desc", description="Sort order (asc/desc)")


# ============================================================================
# Task List Endpoint (GET /api/tasks)
# ============================================================================

@router.get(
    "",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of user's tasks"},
        401: {"description": "Not authenticated"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
    summary="List User's Tasks",
    description="""
Retrieve paginated list of authenticated user's tasks.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Query Parameters:**
- `skip` (int, default=0): Number of tasks to skip (for pagination)
- `limit` (int, default=10): Number of tasks per page (max 100)
- `status` (str, optional): Filter by status ("Pending", "Completed")
- `sort_by` (str, default="created_at"): Sort field ("created_at", "title", "status")
- `order` (str, default="desc"): Sort order ("asc", "desc")

**Success Response (200):**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "Pending",
    "priority": "Medium",
    "created_at": "2025-01-01T10:00:00",
    "updated_at": "2025-01-01T10:00:00",
    "completed_at": null,
    "user_id": "uuid-here"
  }
]
```

**Error Responses:**
- `401`: Not authenticated
- `422`: Validation error
- `500`: Server error

**Security:** Tasks auto-filtered by user_id (multi-user isolation).
    """,
)
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List user's tasks with pagination and filtering.

    Args:
        skip: Number of tasks to skip
        limit: Number of tasks per page
        status: Optional status filter
        sort_by: Field to sort by
        order: Sort order (asc/desc)
        db: Database session
        current_user: Authenticated user

    Returns:
        List[TaskResponse]: Paginated list of user's tasks
    """
    try:
        # Build base query - only user's tasks
        query = db.query(Task).filter(Task.user_id == current_user.id)

        # Apply status filter if provided
        # Map frontend status values (lowercase) to backend status values (Title Case)
        if status:
            status_map = {
                "pending": "Pending",
                "in_progress": "In Progress",
                "completed": "Completed",
                "Pending": "Pending",
                "In Progress": "In Progress",
                "Completed": "Completed",
            }
            mapped_status = status_map.get(status, status)
            query = query.filter(Task.status == mapped_status)

        # Determine sort column
        if sort_by == "title":
            sort_column = Task.title
        elif sort_by == "status":
            sort_column = Task.status
        else:  # default to created_at
            sort_column = Task.created_at

        # Apply sorting
        if order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Get total count
        total = query.count()

        # Apply pagination
        tasks = query.offset(skip).limit(limit).all()

        logger.info(f"User {current_user.id} listed {len(tasks)} tasks")

        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                priority=task.priority,
                created_at=task.created_at,
                updated_at=task.updated_at,
                completed_at=task.completed_at,
                user_id=task.user_id,
            )
            for task in tasks
        ]

    except Exception as e:
        logger.error(f"List tasks error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks",
        )


# ============================================================================
# Create Task Endpoint (POST /api/tasks)
# ============================================================================

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid task data"},
        401: {"description": "Not authenticated"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
    summary="Create New Task",
    description="""
Create a new task for authenticated user.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Request Body:**
- `title` (str, required): Task title (1-200 characters)
- `description` (str, optional): Task description (up to 1000 characters)
- `status` (str, optional): Task status (default "Pending")
- `priority` (str, optional): Task priority (default "Medium")

**Success Response (201):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Pending",
  "priority": "Medium",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T15:30:00",
  "completed_at": null,
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `400`: Invalid input
- `401`: Not authenticated
- `422`: Validation error
- `500`: Server error

**Security:** Task automatically associated with authenticated user.
    """,
)
async def create_task(
    task_create: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create new task for authenticated user.

    Args:
        task_create: Task creation data
        db: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Created task with assigned ID
    """
    try:
        # Create task
        new_task = Task(
            user_id=current_user.id,
            title=task_create.title,
            description=task_create.description,
            status="Pending",
            priority=task_create.priority or "Medium",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        logger.info(f"User {current_user.id} created task {new_task.id}")

        return TaskResponse(
            id=new_task.id,
            title=new_task.title,
            description=new_task.description,
            status=new_task.status,
            priority=new_task.priority,
            created_at=new_task.created_at,
            updated_at=new_task.updated_at,
            completed_at=new_task.completed_at,
            user_id=new_task.user_id,
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Create task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )


# ============================================================================
# Get Task Endpoint (GET /api/tasks/{id})
# ============================================================================

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Task details"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied (not task owner)"},
        404: {"description": "Task not found"},
        500: {"description": "Internal server error"},
    },
    summary="Get Task Details",
    description="""
Retrieve details of a specific task.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Path Parameters:**
- `task_id` (int): ID of the task to retrieve

**Success Response (200):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Pending",
  "priority": "Medium",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T15:30:00",
  "completed_at": null,
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `401`: Not authenticated
- `403`: Access denied (not task owner)
- `404`: Task not found
- `500`: Server error

**Security:** Only task owner can view task details.
    """,
)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get task details.

    Args:
        task_id: ID of task to retrieve
        db: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Task details
    """
    try:
        # Get task
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Check ownership
        if task.user_id != current_user.id:
            logger.warning(f"User {current_user.id} attempted unauthorized access to task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            user_id=task.user_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task",
        )


# ============================================================================
# Update Task Endpoint (PUT /api/tasks/{id})
# ============================================================================

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Task updated successfully"},
        400: {"description": "Invalid task data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied (not task owner)"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
    summary="Update Task",
    description="""
Update an existing task.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Path Parameters:**
- `task_id` (int): ID of the task to update

**Request Body:**
- `title` (str, optional): New task title
- `description` (str, optional): New task description
- `status` (str, optional): New task status
- `priority` (str, optional): New task priority

**Success Response (200):**
```json
{
  "id": 42,
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "status": "In Progress",
  "priority": "High",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T16:45:00",
  "completed_at": null,
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `400`: Invalid input
- `401`: Not authenticated
- `403`: Access denied
- `404`: Task not found
- `422`: Validation error
- `500`: Server error

**Security:** Only task owner can update task.
    """,
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update existing task.

    Args:
        task_id: ID of task to update
        task_update: Task update data
        db: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Updated task
    """
    try:
        # Get task
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Check ownership
        if task.user_id != current_user.id:
            logger.warning(f"User {current_user.id} attempted unauthorized update to task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        # Update fields if provided
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.status is not None:
            task.status = task_update.status
        if task_update.priority is not None:
            task.priority = task_update.priority

        task.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(task)

        logger.info(f"User {current_user.id} updated task {task_id}")

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            user_id=task.user_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Update task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )


# ============================================================================
# Delete Task Endpoint (DELETE /api/tasks/{id})
# ============================================================================

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Task deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied (not task owner)"},
        404: {"description": "Task not found"},
        500: {"description": "Internal server error"},
    },
    summary="Delete Task",
    description="""
Delete a task permanently.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Path Parameters:**
- `task_id` (int): ID of the task to delete

**Success Response (204):**
No content returned.

**Error Responses:**
- `401`: Not authenticated
- `403`: Access denied
- `404`: Task not found
- `500`: Server error

**Security:** Only task owner can delete task.
    """,
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete task permanently.

    Args:
        task_id: ID of task to delete
        db: Database session
        current_user: Authenticated user
    """
    try:
        # Get task
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Check ownership
        if task.user_id != current_user.id:
            logger.warning(f"User {current_user.id} attempted unauthorized delete of task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        # Delete task
        db.delete(task)
        db.commit()

        logger.info(f"User {current_user.id} deleted task {task_id}")

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Delete task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )


# ============================================================================
# Complete Task Endpoint (PATCH /api/tasks/{id}/complete)
# ============================================================================

@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Task marked as completed"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied (not task owner)"},
        404: {"description": "Task not found"},
        409: {"description": "Task already completed"},
        500: {"description": "Internal server error"},
    },
    summary="Mark Task Complete",
    description="""
Mark a task as completed.

**Headers Required:**
- `Authorization: Bearer {access_token}`

**Path Parameters:**
- `task_id` (int): ID of the task to complete

**Success Response (200):**
```json
{
  "id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Completed",
  "priority": "Medium",
  "created_at": "2025-01-03T15:30:00",
  "updated_at": "2025-01-03T16:45:00",
  "completed_at": "2025-01-03T16:45:00",
  "user_id": "uuid-here"
}
```

**Error Responses:**
- `401`: Not authenticated
- `403`: Access denied
- `404`: Task not found
- `409`: Task already completed
- `500`: Server error

**What This Does:**
- Sets `status` to "Completed"
- Sets `completed_at` to current timestamp

**Security:** Only task owner can mark task complete.
    """,
)
async def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark task as completed.

    Args:
        task_id: ID of task to complete
        db: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Updated task with status "Completed"
    """
    try:
        # Get task
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Check ownership
        if task.user_id != current_user.id:
            logger.warning(f"User {current_user.id} attempted unauthorized complete of task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        # Check if already completed
        if task.status == "Completed":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Task already completed",
            )

        # Mark as completed
        task.status = "Completed"
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(task)

        logger.info(f"User {current_user.id} completed task {task_id}")

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            user_id=task.user_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Complete task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete task",
        )
