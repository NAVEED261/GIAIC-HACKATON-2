"""
Recurring Task Service - Phase-5
Handles recurring task logic and scheduling

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import Session, select
from models.task import Task, RecurrencePattern


class RecurringTaskService:
    """
    Service for managing recurring tasks

    Features:
    - Calculate next occurrence dates
    - Create new task instances
    - Handle skip/complete operations
    - Integrate with Kafka for events
    """

    def __init__(self, session: Session, kafka_publisher=None):
        self.session = session
        self.kafka = kafka_publisher

    def calculate_next_occurrence(
        self,
        pattern: RecurrencePattern,
        interval: int = 1,
        from_date: datetime = None
    ) -> datetime:
        """
        Calculate the next occurrence date based on pattern

        Args:
            pattern: RecurrencePattern (daily/weekly/monthly/custom)
            interval: Every N units
            from_date: Base date for calculation

        Returns:
            Next occurrence datetime
        """
        from_date = from_date or datetime.utcnow()

        if pattern == RecurrencePattern.DAILY:
            return from_date + timedelta(days=interval)

        elif pattern == RecurrencePattern.WEEKLY:
            return from_date + timedelta(weeks=interval)

        elif pattern == RecurrencePattern.MONTHLY:
            # Handle month calculation properly
            month = from_date.month + interval
            year = from_date.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            # Handle day overflow (e.g., Jan 31 -> Feb 28)
            day = min(from_date.day, 28)
            return from_date.replace(year=year, month=month, day=day)

        else:  # CUSTOM - treat as days
            return from_date + timedelta(days=interval)

    async def create_recurring_task(
        self,
        user_id: int,
        title: str,
        description: Optional[str] = None,
        pattern: RecurrencePattern = RecurrencePattern.WEEKLY,
        interval: int = 1,
        start_date: datetime = None,
        **kwargs
    ) -> Task:
        """
        Create a new recurring task

        Returns the parent task with next_occurrence set
        """
        start_date = start_date or datetime.utcnow()
        next_occurrence = self.calculate_next_occurrence(pattern, interval, start_date)

        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            is_recurring=True,
            recurrence_pattern=pattern,
            recurrence_interval=interval,
            next_occurrence=next_occurrence,
            **kwargs
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "recurring_task_created",
                "task_id": task.id,
                "user_id": user_id,
                "pattern": pattern.value,
                "interval": interval,
                "next_occurrence": next_occurrence.isoformat()
            })

        return task

    async def complete_recurring_task(self, task_id: int) -> dict:
        """
        Complete a recurring task and create next instance

        1. Mark current task as completed
        2. Calculate next occurrence
        3. Create new task instance
        4. Publish event
        """
        task = self.session.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}

        if not task.is_recurring:
            # Just complete non-recurring task
            task.completed = True
            task.updated_at = datetime.utcnow()
            self.session.commit()
            return {"task_id": task_id, "completed": True}

        # Mark current as completed
        task.completed = True
        task.updated_at = datetime.utcnow()

        # Calculate next occurrence
        next_date = self.calculate_next_occurrence(
            task.recurrence_pattern,
            task.recurrence_interval,
            task.next_occurrence or datetime.utcnow()
        )

        # Create new task instance
        new_task = Task(
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            is_recurring=True,
            recurrence_pattern=task.recurrence_pattern,
            recurrence_interval=task.recurrence_interval,
            parent_task_id=task.parent_task_id or task.id,
            next_occurrence=self.calculate_next_occurrence(
                task.recurrence_pattern,
                task.recurrence_interval,
                next_date
            ),
            due_date=next_date
        )

        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "recurring_task_completed",
                "completed_task_id": task_id,
                "new_task_id": new_task.id,
                "user_id": task.user_id,
                "next_occurrence": next_date.isoformat()
            })

        return {
            "completed_task_id": task_id,
            "new_task_id": new_task.id,
            "next_occurrence": next_date.isoformat()
        }

    async def skip_occurrence(self, task_id: int) -> dict:
        """
        Skip the next occurrence of a recurring task

        Updates next_occurrence to skip one cycle
        """
        task = self.session.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}

        if not task.is_recurring:
            return {"error": "Task is not recurring"}

        # Calculate next-next occurrence (skip one)
        current_next = task.next_occurrence or datetime.utcnow()
        skipped_to = self.calculate_next_occurrence(
            task.recurrence_pattern,
            task.recurrence_interval,
            current_next
        )

        task.next_occurrence = skipped_to
        task.updated_at = datetime.utcnow()
        self.session.commit()

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "recurring_task_skipped",
                "task_id": task_id,
                "skipped_date": current_next.isoformat(),
                "next_occurrence": skipped_to.isoformat()
            })

        return {
            "task_id": task_id,
            "skipped_date": current_next.isoformat(),
            "next_occurrence": skipped_to.isoformat()
        }

    async def stop_recurring(self, task_id: int) -> dict:
        """
        Stop a recurring task series

        Sets is_recurring to False
        """
        task = self.session.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}

        task.is_recurring = False
        task.recurrence_pattern = None
        task.next_occurrence = None
        task.updated_at = datetime.utcnow()
        self.session.commit()

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("task-events", {
                "event_type": "recurring_task_stopped",
                "task_id": task_id,
                "user_id": task.user_id
            })

        return {"task_id": task_id, "is_recurring": False}

    def get_recurring_series(self, parent_task_id: int) -> List[Task]:
        """
        Get all instances of a recurring task series
        """
        statement = select(Task).where(
            (Task.id == parent_task_id) |
            (Task.parent_task_id == parent_task_id)
        ).order_by(Task.created_at)

        return self.session.exec(statement).all()

    def get_due_recurring_tasks(self, before: datetime = None) -> List[Task]:
        """
        Get recurring tasks that are due for next occurrence
        """
        before = before or datetime.utcnow()

        statement = select(Task).where(
            Task.is_recurring == True,
            Task.next_occurrence <= before,
            Task.completed == False
        ).order_by(Task.next_occurrence)

        return self.session.exec(statement).all()
