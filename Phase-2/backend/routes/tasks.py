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

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from db import get_db
from models.task import Task, TaskResponse, TaskCreate, TaskUpdate
from models.user import User

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


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
  },
  ...
]
```

**Error Responses:**
- `401`: Not authenticated (missing or invalid token)
- `500`: Server error

**Pagination Example:**
- Get first 10: `GET /api/tasks?skip=0&limit=10`
- Get next 10: `GET /api/tasks?skip=10&limit=10`
- Get page 3: `GET /api/tasks?skip=20&limit=10`

**Security:** Tasks are automatically filtered by user_id (multi-user isolation).
    """,
)
async def list_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of tasks per page (max 100)"),
    status: Optional[str] = Query(None, description="Filter by status"),
    sort_by: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: None),  # TODO: use get_current_user
):
    """
    List user's tasks with pagination and filtering.

    Args:
        skip: Number of tasks to skip
        limit: Number of tasks per page (max 100)
        status: Optional status filter
        sort_by: Field to sort by
        order: Sort order (asc/desc)
        db: Database session
        current_user: Authenticated user

    Returns:
        List[TaskResponse]: Paginated list of user's tasks

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 500: Server error
    """
    # TODO: Implement task list logic
    # 1. Validate user is authenticated
    # 2. Query tasks filtered by user_id
    # 3. Apply status filter if provided
    # 4. Sort by specified field and order
    # 5. Apply pagination (skip/limit)
    # 6. Return list of TaskResponse objects
    pass


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
- `400`: Invalid input (empty title, title too long)
- `401`: Not authenticated
- `500`: Server error

**Field Constraints:**
- `title`: Required, 1-200 characters
- `description`: Optional, up to 1000 characters
- `status`: Optional, defaults to "Pending"
- `priority`: Optional, defaults to "Medium"

**Security:** Task automatically associated with authenticated user.
    """,
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: None),  # TODO: use get_current_user
):
    """
    Create new task for authenticated user.

    Args:
        task: Task creation data
        db: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Created task with assigned ID

    Raises:
        HTTPException 400: Invalid task data
        HTTPException 401: Not authenticated
        HTTPException 500: Server error
    """
    # TODO: Implement task creation logic
    # 1. Validate user is authenticated
    # 2. Validate task data (title not empty, within limits)
    # 3. Create task record with user_id from current_user
    # 4. Set default status and priority if not provided
    # 5. Auto-generate created_at and updated_at timestamps
    # 6. Commit to database
    # 7. Return TaskResponse with new task ID
    pass


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
- `403`: Access denied (task belongs to different user)
- `404`: Task not found
- `500`: Server error

**Security:** Only task owner can view task details (enforced via user_id check).
    """,
)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: None),  # TODO: use get_current_user
):
    """
    Get task details.

    Args:
        task_id: ID of task to retrieve
        db: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Task details

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Access denied
        HTTPException 404: Task not found
        HTTPException 500: Server error
    """
    # TODO: Implement get task logic
    # 1. Validate user is authenticated
    # 2. Query task by ID
    # 3. Check task exists (404 if not)
    # 4. Check task belongs to current user (403 if not)
    # 5. Return TaskResponse
    pass


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
- `403`: Access denied (task belongs to different user)
- `404`: Task not found
- `500`: Server error

**Partial Updates:**
Send only fields you want to update. Unspecified fields remain unchanged.

**Security:** Only task owner can update task (enforced via user_id check).
    """,
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: None),  # TODO: use get_current_user
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

    Raises:
        HTTPException 400: Invalid data
        HTTPException 401: Not authenticated
        HTTPException 403: Access denied
        HTTPException 404: Task not found
        HTTPException 500: Server error
    """
    # TODO: Implement task update logic
    # 1. Validate user is authenticated
    # 2. Query task by ID (404 if not found)
    # 3. Check task belongs to current user (403 if not)
    # 4. Update only specified fields
    # 5. Update updated_at timestamp
    # 6. Commit changes
    # 7. Return updated TaskResponse
    pass


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
- `403`: Access denied (task belongs to different user)
- `404`: Task not found
- `500`: Server error

**Note:** This is a hard delete. Consider soft delete if audit trail needed.

**Security:** Only task owner can delete task (enforced via user_id check).
    """,
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: None),  # TODO: use get_current_user
):
    """
    Delete task permanently.

    Args:
        task_id: ID of task to delete
        db: Database session
        current_user: Authenticated user

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Access denied
        HTTPException 404: Task not found
        HTTPException 500: Server error
    """
    # TODO: Implement task delete logic
    # 1. Validate user is authenticated
    # 2. Query task by ID (404 if not found)
    # 3. Check task belongs to current user (403 if not)
    # 4. Delete task from database
    # 5. Commit changes
    # 6. Return 204 No Content
    pass


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
- `403`: Access denied (task belongs to different user)
- `404`: Task not found
- `409`: Task already completed
- `500`: Server error

**What This Does:**
- Sets `status` to "Completed"
- Sets `completed_at` to current timestamp
- Updates `updated_at` timestamp

**Security:** Only task owner can mark task complete (enforced via user_id check).
    """,
)
async def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: None),  # TODO: use get_current_user
):
    """
    Mark task as completed.

    Args:
        task_id: ID of task to complete
        db: Database session
        current_user: Authenticated user

    Returns:
        TaskResponse: Updated task with status "Completed"

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Access denied
        HTTPException 404: Task not found
        HTTPException 409: Already completed
        HTTPException 500: Server error
    """
    # TODO: Implement complete task logic
    # 1. Validate user is authenticated
    # 2. Query task by ID (404 if not found)
    # 3. Check task belongs to current user (403 if not)
    # 4. Check task not already completed (409 if it is)
    # 5. Set status to "Completed"
    # 6. Set completed_at to current timestamp
    # 7. Update updated_at timestamp
    # 8. Commit changes
    # 9. Return updated TaskResponse
    pass
