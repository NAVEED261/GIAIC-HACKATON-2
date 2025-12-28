"""
Task Service - Phase-5
Handles task CRUD with advanced features

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select, or_, and_
from models.task import Task, TaskCreate, TaskUpdate, TaskFilter, Priority
from models.tag import Tag, TaskTag


class TaskService:
    """
    Service for managing tasks with Phase-5 features

    Features:
    - CRUD operations
    - Priority management
    - Tag management
    - Search, filter, sort
    - Overdue detection
    """

    def __init__(self, session: Session, kafka_publisher=None):
        self.session = session
        self.kafka = kafka_publisher

    async def create_task(self, user_id: int, task_data: TaskCreate) -> Task:
        """Create a new task"""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority or Priority.MEDIUM,
            due_date=task_data.due_date,
            is_recurring=task_data.is_recurring,
            recurrence_pattern=task_data.recurrence_pattern,
            recurrence_interval=task_data.recurrence_interval
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        # Add tags if provided
        if task_data.tag_ids:
            await self.add_tags(task.id, task_data.tag_ids)

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "task_created",
                "task_id": task.id,
                "user_id": user_id,
                "priority": task.priority.value
            })

        return task

    async def update_task(
        self,
        task_id: int,
        user_id: int,
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """Update a task"""
        task = self.session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return None

        # Update fields
        update_data = task_data.model_dump(exclude_unset=True)
        tag_ids = update_data.pop("tag_ids", None)

        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(task)

        # Update tags if provided
        if tag_ids is not None:
            await self.set_tags(task.id, tag_ids)

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "task_updated",
                "task_id": task.id,
                "user_id": user_id,
                "changes": list(update_data.keys())
            })

        return task

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task"""
        task = self.session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return False

        self.session.delete(task)
        self.session.commit()

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "task_deleted",
                "task_id": task_id,
                "user_id": user_id
            })

        return True

    def get_task(self, task_id: int, user_id: int) -> Optional[Task]:
        """Get a single task"""
        task = self.session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return None

        return task

    def get_tasks(
        self,
        user_id: int,
        filter_params: Optional[TaskFilter] = None
    ) -> List[Task]:
        """
        Get tasks with filtering and sorting

        Supports:
        - Status filter (completed/pending/all)
        - Priority filter
        - Recurring filter
        - Due date filter
        - Overdue filter
        - Tag filter
        - Full-text search
        - Sorting
        """
        statement = select(Task).where(Task.user_id == user_id)

        if filter_params:
            # Status filter
            if filter_params.status == "completed":
                statement = statement.where(Task.completed == True)
            elif filter_params.status == "pending":
                statement = statement.where(Task.completed == False)

            # Priority filter
            if filter_params.priority:
                statement = statement.where(Task.priority == filter_params.priority)

            # Recurring filter
            if filter_params.is_recurring is not None:
                statement = statement.where(Task.is_recurring == filter_params.is_recurring)

            # Due date filter
            if filter_params.has_due_date is not None:
                if filter_params.has_due_date:
                    statement = statement.where(Task.due_date.isnot(None))
                else:
                    statement = statement.where(Task.due_date.is_(None))

            # Overdue filter
            if filter_params.is_overdue:
                statement = statement.where(
                    Task.due_date < datetime.utcnow(),
                    Task.completed == False
                )

            # Search
            if filter_params.search:
                search_term = f"%{filter_params.search}%"
                statement = statement.where(
                    or_(
                        Task.title.ilike(search_term),
                        Task.description.ilike(search_term)
                    )
                )

            # Tag filter
            if filter_params.tag_ids:
                statement = statement.join(TaskTag).where(
                    TaskTag.tag_id.in_(filter_params.tag_ids)
                )

            # Sorting
            sort_column = getattr(Task, filter_params.sort_by or "created_at", Task.created_at)
            if filter_params.sort_order == "asc":
                statement = statement.order_by(sort_column.asc())
            else:
                statement = statement.order_by(sort_column.desc())

        else:
            statement = statement.order_by(Task.created_at.desc())

        return self.session.exec(statement).all()

    # ==================== Tag Management ====================

    async def add_tags(self, task_id: int, tag_ids: List[int]) -> bool:
        """Add tags to a task"""
        for tag_id in tag_ids:
            # Check if already exists
            existing = self.session.exec(
                select(TaskTag).where(
                    TaskTag.task_id == task_id,
                    TaskTag.tag_id == tag_id
                )
            ).first()

            if not existing:
                task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
                self.session.add(task_tag)

        self.session.commit()
        return True

    async def remove_tags(self, task_id: int, tag_ids: List[int]) -> bool:
        """Remove tags from a task"""
        for tag_id in tag_ids:
            task_tag = self.session.exec(
                select(TaskTag).where(
                    TaskTag.task_id == task_id,
                    TaskTag.tag_id == tag_id
                )
            ).first()

            if task_tag:
                self.session.delete(task_tag)

        self.session.commit()
        return True

    async def set_tags(self, task_id: int, tag_ids: List[int]) -> bool:
        """Set tags for a task (replace all)"""
        # Remove all existing
        existing = self.session.exec(
            select(TaskTag).where(TaskTag.task_id == task_id)
        ).all()

        for task_tag in existing:
            self.session.delete(task_tag)

        # Add new
        for tag_id in tag_ids:
            task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
            self.session.add(task_tag)

        self.session.commit()
        return True

    # ==================== Priority Management ====================

    async def set_priority(self, task_id: int, user_id: int, priority: Priority) -> Optional[Task]:
        """Set task priority"""
        task = self.session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return None

        old_priority = task.priority
        task.priority = priority
        task.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(task)

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "priority_changed",
                "task_id": task_id,
                "user_id": user_id,
                "old_priority": old_priority.value,
                "new_priority": priority.value
            })

        return task

    # ==================== Due Date Management ====================

    async def set_due_date(
        self,
        task_id: int,
        user_id: int,
        due_date: Optional[datetime]
    ) -> Optional[Task]:
        """Set task due date"""
        task = self.session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return None

        task.due_date = due_date
        task.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(task)

        return task

    # ==================== Statistics ====================

    def get_statistics(self, user_id: int) -> dict:
        """Get task statistics for a user"""
        all_tasks = self.session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()

        total = len(all_tasks)
        completed = sum(1 for t in all_tasks if t.completed)
        overdue = sum(1 for t in all_tasks if t.due_date and t.due_date < datetime.utcnow() and not t.completed)
        recurring = sum(1 for t in all_tasks if t.is_recurring)

        priority_counts = {
            "low": sum(1 for t in all_tasks if t.priority == Priority.LOW),
            "medium": sum(1 for t in all_tasks if t.priority == Priority.MEDIUM),
            "high": sum(1 for t in all_tasks if t.priority == Priority.HIGH),
            "urgent": sum(1 for t in all_tasks if t.priority == Priority.URGENT),
        }

        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "overdue": overdue,
            "recurring": recurring,
            "by_priority": priority_counts
        }
