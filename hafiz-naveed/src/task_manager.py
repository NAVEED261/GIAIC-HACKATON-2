"""
TodoActionAgent: Task Management and Operations

This module implements the TodoActionAgent sub-agent that handles
all task operations (CRUD), maintains in-memory storage, and
ensures data integrity.
"""

from typing import List, Optional
from models import Task


class TodoActionAgent:
    """
    Sub-agent responsible for executing all task operations.

    Maintains an in-memory list of tasks and provides methods for:
    - Creating new tasks
    - Retrieving tasks
    - Updating tasks
    - Deleting tasks
    - Marking tasks as completed
    - Validating operations
    """

    def __init__(self) -> None:
        """Initialize TodoActionAgent with empty task list and ID counter."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        """
        Add a new task with auto-generated unique ID.

        Args:
            title: Task description (must be non-empty)

        Returns:
            Newly created Task object

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Validate title
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title cannot be empty")

        # Create task with next ID
        task = Task(task_id=self._next_id, title=title, status="Pending")
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the store.

        Returns:
            List of all Task objects in order
        """
        return self._tasks.copy()

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Find a specific task by ID.

        Args:
            task_id: Task ID to search for

        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_title: str) -> bool:
        """
        Update a task's title by ID.

        Args:
            task_id: ID of task to update
            new_title: New task description

        Returns:
            True if successful, False if task not found

        Raises:
            ValueError: If new_title is empty or whitespace-only
        """
        # Validate new title
        if not isinstance(new_title, str) or not new_title.strip():
            raise ValueError("Task title cannot be empty")

        # Find and update task
        task = self.get_task(task_id)
        if task:
            task.update_title(new_title)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            True if successful, False if task not found
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as completed by ID.

        Args:
            task_id: ID of task to mark complete

        Returns:
            True if successful, False if task not found
        """
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            return True
        return False
