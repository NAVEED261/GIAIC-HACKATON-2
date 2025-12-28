"""
Reminder Service - Phase-5
Handles reminder logic and notifications

@author: Phase-5 System
@specs: Phase-5/specs/features/part-a-advanced-features.md
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import Session, select
from models.reminder import Reminder, ReminderStatus, ReminderType
from models.task import Task


class ReminderService:
    """
    Service for managing task reminders

    Features:
    - Create/update/cancel reminders
    - Snooze functionality
    - Due date auto-reminders
    - Overdue detection
    - Integration with Dapr for scheduling
    """

    def __init__(self, session: Session, dapr_client=None, kafka_publisher=None):
        self.session = session
        self.dapr = dapr_client
        self.kafka = kafka_publisher

    async def create_reminder(
        self,
        task_id: int,
        user_id: int,
        remind_at: datetime,
        reminder_type: ReminderType = ReminderType.PUSH,
        message: Optional[str] = None
    ) -> Reminder:
        """
        Create a new reminder for a task
        """
        reminder = Reminder(
            task_id=task_id,
            user_id=user_id,
            remind_at=remind_at,
            reminder_type=reminder_type,
            message=message,
            status=ReminderStatus.PENDING
        )

        self.session.add(reminder)
        self.session.commit()
        self.session.refresh(reminder)

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("reminders", {
                "event_type": "reminder_scheduled",
                "reminder_id": reminder.id,
                "task_id": task_id,
                "user_id": user_id,
                "remind_at": remind_at.isoformat(),
                "type": reminder_type.value
            })

        # Schedule with Dapr if available
        if self.dapr:
            await self._schedule_with_dapr(reminder)

        return reminder

    async def _schedule_with_dapr(self, reminder: Reminder):
        """Schedule reminder using Dapr cron binding"""
        try:
            # Using Dapr binding for scheduling
            await self.dapr.invoke_binding(
                "reminder-cron",
                "create",
                data={
                    "reminder_id": reminder.id,
                    "task_id": reminder.task_id,
                    "user_id": reminder.user_id,
                    "remind_at": reminder.remind_at.isoformat()
                }
            )
        except Exception as e:
            print(f"Failed to schedule with Dapr: {e}")

    async def cancel_reminder(self, reminder_id: int, user_id: int) -> dict:
        """Cancel a reminder"""
        reminder = self.session.get(Reminder, reminder_id)

        if not reminder:
            return {"error": "Reminder not found"}

        if reminder.user_id != user_id:
            return {"error": "Not authorized"}

        reminder.status = ReminderStatus.CANCELLED
        reminder.updated_at = datetime.utcnow()
        self.session.commit()

        # Publish Kafka event
        if self.kafka:
            await self.kafka.publish("reminders", {
                "event_type": "reminder_cancelled",
                "reminder_id": reminder_id,
                "task_id": reminder.task_id,
                "user_id": user_id
            })

        return {"reminder_id": reminder_id, "status": "cancelled"}

    async def snooze_reminder(
        self,
        reminder_id: int,
        user_id: int,
        snooze_minutes: int = 15
    ) -> dict:
        """Snooze a reminder for later"""
        reminder = self.session.get(Reminder, reminder_id)

        if not reminder:
            return {"error": "Reminder not found"}

        if reminder.user_id != user_id:
            return {"error": "Not authorized"}

        new_time = datetime.utcnow() + timedelta(minutes=snooze_minutes)
        reminder.status = ReminderStatus.SNOOZED
        reminder.snoozed_until = new_time
        reminder.remind_at = new_time
        reminder.updated_at = datetime.utcnow()
        self.session.commit()

        # Reschedule with Dapr
        if self.dapr:
            await self._schedule_with_dapr(reminder)

        return {
            "reminder_id": reminder_id,
            "status": "snoozed",
            "snoozed_until": new_time.isoformat()
        }

    async def mark_sent(self, reminder_id: int) -> dict:
        """Mark a reminder as sent"""
        reminder = self.session.get(Reminder, reminder_id)

        if not reminder:
            return {"error": "Reminder not found"}

        reminder.status = ReminderStatus.SENT
        reminder.sent_at = datetime.utcnow()
        reminder.updated_at = datetime.utcnow()
        self.session.commit()

        return {"reminder_id": reminder_id, "status": "sent"}

    def get_upcoming_reminders(
        self,
        user_id: int,
        days_ahead: int = 7
    ) -> List[Reminder]:
        """Get upcoming reminders for a user"""
        end_date = datetime.utcnow() + timedelta(days=days_ahead)

        statement = select(Reminder).where(
            Reminder.user_id == user_id,
            Reminder.status == ReminderStatus.PENDING,
            Reminder.remind_at >= datetime.utcnow(),
            Reminder.remind_at <= end_date
        ).order_by(Reminder.remind_at)

        return self.session.exec(statement).all()

    def get_overdue_tasks(self, user_id: int) -> List[Task]:
        """Get all overdue tasks for a user"""
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.due_date < datetime.utcnow(),
            Task.completed == False
        ).order_by(Task.due_date)

        return self.session.exec(statement).all()

    def get_due_today(self, user_id: int) -> List[Task]:
        """Get tasks due today"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        statement = select(Task).where(
            Task.user_id == user_id,
            Task.due_date >= today_start,
            Task.due_date < today_end,
            Task.completed == False
        ).order_by(Task.due_date)

        return self.session.exec(statement).all()

    async def create_auto_reminder(
        self,
        task_id: int,
        user_id: int,
        due_date: datetime,
        advance_minutes: int = 60
    ) -> Optional[Reminder]:
        """
        Create an automatic reminder before task due date

        Args:
            task_id: Task ID
            user_id: User ID
            due_date: Task due date
            advance_minutes: How many minutes before to remind

        Returns:
            Created reminder or None if due_date is in the past
        """
        remind_at = due_date - timedelta(minutes=advance_minutes)

        if remind_at <= datetime.utcnow():
            return None

        return await self.create_reminder(
            task_id=task_id,
            user_id=user_id,
            remind_at=remind_at,
            reminder_type=ReminderType.PUSH,
            message=f"Task due in {advance_minutes} minutes"
        )

    def get_pending_notifications(self, limit: int = 100) -> List[Reminder]:
        """
        Get reminders that need to be sent now

        Used by notification worker to process due reminders
        """
        statement = select(Reminder).where(
            Reminder.status == ReminderStatus.PENDING,
            Reminder.remind_at <= datetime.utcnow()
        ).order_by(Reminder.remind_at).limit(limit)

        return self.session.exec(statement).all()

    async def process_due_reminders(self) -> List[dict]:
        """
        Process all due reminders

        This is called by the Dapr cron binding
        """
        reminders = self.get_pending_notifications()
        results = []

        for reminder in reminders:
            try:
                # Publish notification event
                if self.kafka:
                    await self.kafka.publish("notifications", {
                        "event_type": "send_notification",
                        "reminder_id": reminder.id,
                        "task_id": reminder.task_id,
                        "user_id": reminder.user_id,
                        "type": reminder.reminder_type.value,
                        "message": reminder.message
                    })

                # Mark as sent
                await self.mark_sent(reminder.id)
                results.append({
                    "reminder_id": reminder.id,
                    "status": "processed"
                })

            except Exception as e:
                reminder.status = ReminderStatus.FAILED
                self.session.commit()
                results.append({
                    "reminder_id": reminder.id,
                    "status": "failed",
                    "error": str(e)
                })

        return results
