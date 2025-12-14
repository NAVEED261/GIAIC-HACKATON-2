"""
Task Model for Phase-1 Todo System

This module defines the Task data structure with validation,
serialization, and status management capabilities.
"""

from typing import Dict, Any


class Task:
    """
    Represents a single todo task with id, title, and status.

    Attributes:
        id (int): Unique identifier for the task (auto-assigned)
        title (str): Task description (required, non-empty)
        status (str): Task status - either "Pending" or "Completed"
    """

    def __init__(self, task_id: int, title: str, status: str = "Pending") -> None:
        """
        Initialize a new Task.

        Args:
            task_id: Unique integer identifier
            title: Task description (must be non-empty)
            status: Task status, defaults to "Pending"

        Raises:
            ValueError: If title is empty or whitespace-only
            ValueError: If status is not "Pending" or "Completed"
        """
        # Validate task_id
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer")

        # Validate title
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate status
        if status not in ("Pending", "Completed"):
            raise ValueError('Status must be either "Pending" or "Completed"')

        self.id: int = task_id
        self.title: str = title.strip()
        self.status: str = status

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary representation for display.

        Returns:
            Dictionary with id, title, and status keys
        """
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status
        }

    def update_title(self, new_title: str) -> None:
        """
        Update task title with validation.

        Args:
            new_title: New task description

        Raises:
            ValueError: If new_title is empty or whitespace-only
        """
        if not isinstance(new_title, str) or not new_title.strip():
            raise ValueError("Task title cannot be empty")
        self.title = new_title.strip()

    def mark_complete(self) -> None:
        """Mark task as completed by setting status to 'Completed'."""
        self.status = "Completed"

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"[{self.id}] {self.title} ({self.status})"
