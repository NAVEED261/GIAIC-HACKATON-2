"""
Reminder Agent - Reminders & Due Dates Expert
Handles reminder scheduling for Phase-5

@author: Phase-5 AI Employs System
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class ReminderAgent(BaseAgent):
    """
    Reminders & Due Dates Expert Agent

    Capabilities:
    - Set and manage reminders
    - Due date management
    - Notification scheduling
    - Overdue detection
    - Reminder preferences

    MCP Tools: 10
    """

    def __init__(self):
        super().__init__()
        self.name = "ReminderAgent"
        self.domain = "reminder"
        self.description = "Reminders and due dates expert"
        self.emoji = "⏰"

        # Reminder types
        self.reminder_types = {
            "email": {"channel": "email", "priority": "normal"},
            "push": {"channel": "push_notification", "priority": "high"},
            "sms": {"channel": "sms", "priority": "urgent"},
            "in_app": {"channel": "in_app", "priority": "normal"}
        }

    def _setup_tools(self):
        """Setup Reminder MCP tools"""

        # Tool 1: Set Reminder
        self.register_tool(MCPTool(
            name="set_reminder",
            description="Set a reminder for a task",
            parameters={
                "task_id": "int (required)",
                "remind_at": "string (ISO datetime)",
                "reminder_type": "string (email/push/sms/in_app)",
                "message": "string (optional)"
            },
            handler=self._set_reminder
        ))

        # Tool 2: Cancel Reminder
        self.register_tool(MCPTool(
            name="cancel_reminder",
            description="Cancel an existing reminder",
            parameters={"reminder_id": "int (required)"},
            handler=self._cancel_reminder
        ))

        # Tool 3: Set Due Date
        self.register_tool(MCPTool(
            name="set_due_date",
            description="Set or update task due date",
            parameters={
                "task_id": "int (required)",
                "due_date": "string (ISO datetime)",
                "auto_remind": "bool (default: true)"
            },
            handler=self._set_due_date
        ))

        # Tool 4: Get Upcoming Reminders
        self.register_tool(MCPTool(
            name="get_upcoming_reminders",
            description="Get upcoming reminders for user",
            parameters={
                "user_id": "string (required)",
                "days_ahead": "int (default: 7)"
            },
            handler=self._get_upcoming
        ))

        # Tool 5: Get Overdue Tasks
        self.register_tool(MCPTool(
            name="get_overdue_tasks",
            description="Get all overdue tasks for user",
            parameters={"user_id": "string (required)"},
            handler=self._get_overdue
        ))

        # Tool 6: Snooze Reminder
        self.register_tool(MCPTool(
            name="snooze_reminder",
            description="Snooze a reminder for later",
            parameters={
                "reminder_id": "int (required)",
                "snooze_minutes": "int (default: 15)"
            },
            handler=self._snooze_reminder
        ))

        # Tool 7: Get Reminder Types
        self.register_tool(MCPTool(
            name="get_reminder_types",
            description="Get available reminder types",
            parameters={},
            handler=self._get_reminder_types
        ))

        # Tool 8: Update Reminder Preferences
        self.register_tool(MCPTool(
            name="update_reminder_preferences",
            description="Update user's reminder preferences",
            parameters={
                "user_id": "string (required)",
                "default_type": "string",
                "advance_minutes": "int",
                "quiet_hours": "dict"
            },
            handler=self._update_preferences
        ))

        # Tool 9: Schedule Notification
        self.register_tool(MCPTool(
            name="schedule_notification",
            description="Schedule a notification via Dapr",
            parameters={
                "user_id": "string (required)",
                "message": "string (required)",
                "schedule_at": "string (ISO datetime)",
                "channel": "string (email/push/sms)"
            },
            handler=self._schedule_notification
        ))

        # Tool 10: Get Due Today
        self.register_tool(MCPTool(
            name="get_due_today",
            description="Get all tasks due today",
            parameters={"user_id": "string (required)"},
            handler=self._get_due_today
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best Reminder tool"""
        query = query.lower()

        if any(w in query for w in ['set reminder', 'remind me', 'create reminder', 'add reminder']):
            return 'set_reminder'
        elif any(w in query for w in ['cancel reminder', 'remove reminder', 'delete reminder']):
            return 'cancel_reminder'
        elif any(w in query for w in ['due date', 'set due', 'deadline']):
            return 'set_due_date'
        elif any(w in query for w in ['upcoming', 'next reminder', 'future reminder']):
            return 'get_upcoming_reminders'
        elif any(w in query for w in ['overdue', 'past due', 'missed']):
            return 'get_overdue_tasks'
        elif any(w in query for w in ['snooze', 'later', 'postpone']):
            return 'snooze_reminder'
        elif any(w in query for w in ['reminder type', 'notification type']):
            return 'get_reminder_types'
        elif any(w in query for w in ['preference', 'setting', 'configure']):
            return 'update_reminder_preferences'
        elif any(w in query for w in ['schedule notification', 'send notification']):
            return 'schedule_notification'
        elif any(w in query for w in ['due today', 'today task', 'today due']):
            return 'get_due_today'

        return 'get_upcoming_reminders'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'set_reminder':
            return await self._set_reminder(
                task_id=1,
                remind_at=(datetime.utcnow() + timedelta(hours=1)).isoformat()
            )

        elif tool_name == 'cancel_reminder':
            return await self._cancel_reminder(reminder_id=1)

        elif tool_name == 'set_due_date':
            return await self._set_due_date(
                task_id=1,
                due_date=(datetime.utcnow() + timedelta(days=1)).isoformat()
            )

        elif tool_name == 'get_upcoming_reminders':
            return await self._get_upcoming(user_id="user")

        elif tool_name == 'get_overdue_tasks':
            return await self._get_overdue(user_id="user")

        elif tool_name == 'snooze_reminder':
            return await self._snooze_reminder(reminder_id=1)

        elif tool_name == 'get_reminder_types':
            return await self._get_reminder_types()

        elif tool_name == 'update_reminder_preferences':
            return await self._update_preferences(user_id="user")

        elif tool_name == 'schedule_notification':
            return await self._schedule_notification(
                user_id="user",
                message="Test notification",
                schedule_at=(datetime.utcnow() + timedelta(hours=1)).isoformat()
            )

        elif tool_name == 'get_due_today':
            return await self._get_due_today(user_id="user")

        else:
            return await self._get_reminder_types()

    # ==================== Tool Handlers ====================

    async def _set_reminder(self, task_id: int, remind_at: str,
                           reminder_type: str = "push",
                           message: str = None) -> Dict:
        """Set a reminder for a task"""
        remind_datetime = datetime.fromisoformat(remind_at)

        return {
            "status": "success",
            "reminder": {
                "task_id": task_id,
                "remind_at": remind_at,
                "type": reminder_type,
                "message": message or "Task reminder"
            },
            "api_call": f"POST /api/user/tasks/{task_id}/reminders",
            "body": {
                "remind_at": remind_at,
                "reminder_type": reminder_type,
                "message": message
            },
            "kafka_event": {
                "topic": "reminders",
                "event_type": "reminder_scheduled",
                "task_id": task_id,
                "scheduled_for": remind_at
            },
            "dapr_binding": {
                "binding": "cron-binding",
                "operation": "create",
                "schedule": remind_datetime.strftime("%M %H %d %m *"),
                "data": {
                    "task_id": task_id,
                    "user_id": "user",
                    "type": reminder_type
                }
            },
            "mcp_tool_code": """
@tool
async def set_reminder(
    task_id: int,
    remind_at: str,
    reminder_type: str = "push"
):
    reminder = Reminder(
        task_id=task_id,
        remind_at=datetime.fromisoformat(remind_at),
        type=reminder_type
    )
    await save_reminder(reminder)

    # Schedule via Dapr cron binding
    await dapr_client.invoke_binding(
        "cron-binding",
        "create",
        data={"reminder_id": reminder.id}
    )

    # Publish event
    await publish_event("reminders", {
        "event_type": "reminder_scheduled",
        "reminder_id": reminder.id,
        "task_id": task_id
    })

    return {"reminder_id": reminder.id}
"""
        }

    async def _cancel_reminder(self, reminder_id: int) -> Dict:
        """Cancel a reminder"""
        return {
            "status": "success",
            "reminder_id": reminder_id,
            "action": "cancelled",
            "api_call": f"DELETE /api/user/reminders/{reminder_id}",
            "kafka_event": {
                "topic": "reminders",
                "event_type": "reminder_cancelled",
                "reminder_id": reminder_id
            }
        }

    async def _set_due_date(self, task_id: int, due_date: str,
                           auto_remind: bool = True) -> Dict:
        """Set task due date"""
        due_datetime = datetime.fromisoformat(due_date)
        remind_at = due_datetime - timedelta(hours=1)  # 1 hour before

        result = {
            "status": "success",
            "task_id": task_id,
            "due_date": due_date,
            "api_call": f"PATCH /api/user/tasks/{task_id}",
            "body": {"due_date": due_date}
        }

        if auto_remind:
            result["auto_reminder"] = {
                "remind_at": remind_at.isoformat(),
                "type": "push",
                "message": "Task due in 1 hour"
            }

        return result

    async def _get_upcoming(self, user_id: str, days_ahead: int = 7) -> Dict:
        """Get upcoming reminders"""
        return {
            "status": "success",
            "user_id": user_id,
            "days_ahead": days_ahead,
            "api_call": f"GET /api/{user_id}/reminders?days={days_ahead}",
            "sql_query": f"""
SELECT r.*, t.title as task_title
FROM reminders r
JOIN tasks t ON r.task_id = t.id
WHERE t.user_id = '{user_id}'
  AND r.remind_at > NOW()
  AND r.remind_at < NOW() + INTERVAL '{days_ahead} days'
  AND r.status = 'pending'
ORDER BY r.remind_at ASC
"""
        }

    async def _get_overdue(self, user_id: str) -> Dict:
        """Get overdue tasks"""
        return {
            "status": "success",
            "user_id": user_id,
            "api_call": f"GET /api/{user_id}/tasks?filter=overdue",
            "sql_query": f"""
SELECT * FROM tasks
WHERE user_id = '{user_id}'
  AND due_date < NOW()
  AND completed = false
ORDER BY due_date ASC
""",
            "kafka_consumer": {
                "topic": "task-events",
                "filter": "event_type = 'task_overdue'"
            }
        }

    async def _snooze_reminder(self, reminder_id: int,
                              snooze_minutes: int = 15) -> Dict:
        """Snooze a reminder"""
        new_time = datetime.utcnow() + timedelta(minutes=snooze_minutes)

        return {
            "status": "success",
            "reminder_id": reminder_id,
            "snoozed_until": new_time.isoformat(),
            "snooze_minutes": snooze_minutes,
            "api_call": f"POST /api/user/reminders/{reminder_id}/snooze",
            "body": {"minutes": snooze_minutes}
        }

    async def _get_reminder_types(self) -> Dict:
        """Get available reminder types"""
        return {
            "status": "success",
            "types": [
                {
                    "name": "email",
                    "description": "Email notification",
                    "priority": "normal",
                    "delay_allowed": True
                },
                {
                    "name": "push",
                    "description": "Push notification (mobile/web)",
                    "priority": "high",
                    "delay_allowed": False
                },
                {
                    "name": "sms",
                    "description": "SMS text message",
                    "priority": "urgent",
                    "delay_allowed": False
                },
                {
                    "name": "in_app",
                    "description": "In-app notification",
                    "priority": "normal",
                    "delay_allowed": True
                }
            ],
            "default": "push"
        }

    async def _update_preferences(self, user_id: str,
                                  default_type: str = None,
                                  advance_minutes: int = None,
                                  quiet_hours: Dict = None) -> Dict:
        """Update reminder preferences"""
        return {
            "status": "success",
            "user_id": user_id,
            "api_call": f"PATCH /api/{user_id}/preferences/reminders",
            "body": {
                "default_type": default_type or "push",
                "advance_minutes": advance_minutes or 60,
                "quiet_hours": quiet_hours or {"start": "22:00", "end": "08:00"}
            },
            "dapr_state": {
                "store": "statestore",
                "key": f"user-{user_id}-reminder-prefs",
                "value": {
                    "default_type": default_type,
                    "advance_minutes": advance_minutes,
                    "quiet_hours": quiet_hours
                }
            }
        }

    async def _schedule_notification(self, user_id: str, message: str,
                                    schedule_at: str,
                                    channel: str = "push") -> Dict:
        """Schedule a notification via Dapr"""
        return {
            "status": "success",
            "notification": {
                "user_id": user_id,
                "message": message,
                "schedule_at": schedule_at,
                "channel": channel
            },
            "dapr_pubsub": {
                "pubsub": "kafka-pubsub",
                "topic": "reminders",
                "data": {
                    "type": "scheduled_notification",
                    "user_id": user_id,
                    "message": message,
                    "deliver_at": schedule_at,
                    "channel": channel
                }
            },
            "python_code": f"""
import httpx

# Using Dapr pub/sub
await httpx.post(
    "http://localhost:3500/v1.0/publish/kafka-pubsub/reminders",
    json={{
        "type": "scheduled_notification",
        "user_id": "{user_id}",
        "message": "{message}",
        "deliver_at": "{schedule_at}",
        "channel": "{channel}"
    }}
)
"""
        }

    async def _get_due_today(self, user_id: str) -> Dict:
        """Get tasks due today"""
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        return {
            "status": "success",
            "user_id": user_id,
            "date": today.isoformat(),
            "api_call": f"GET /api/{user_id}/tasks?due_date={today.isoformat()}",
            "sql_query": f"""
SELECT * FROM tasks
WHERE user_id = '{user_id}'
  AND due_date >= '{today.isoformat()}'
  AND due_date < '{tomorrow.isoformat()}'
  AND completed = false
ORDER BY due_date ASC, priority DESC
"""
        }
