"""
Recurring Agent - Recurring Tasks Expert
Handles recurring task scheduling for Phase-5

@author: Phase-5 AI Employs System
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class RecurringAgent(BaseAgent):
    """
    Recurring Tasks Expert Agent

    Capabilities:
    - Create recurring tasks
    - Manage recurrence patterns
    - Calculate next occurrences
    - Handle recurring series

    MCP Tools: 8
    """

    def __init__(self):
        super().__init__()
        self.name = "RecurringAgent"
        self.domain = "recurring"
        self.description = "Recurring tasks and scheduling expert"
        self.emoji = "🔄"

        # Recurrence patterns
        self.patterns = {
            "daily": {"unit": "days", "default_interval": 1},
            "weekly": {"unit": "weeks", "default_interval": 1},
            "monthly": {"unit": "months", "default_interval": 1},
            "custom": {"unit": "days", "default_interval": 1}
        }

    def _setup_tools(self):
        """Setup Recurring MCP tools"""

        # Tool 1: Create Recurring Task
        self.register_tool(MCPTool(
            name="create_recurring_task",
            description="Create a recurring task",
            parameters={
                "user_id": "string (required)",
                "title": "string (required)",
                "pattern": "string (daily/weekly/monthly/custom)",
                "interval": "int (default: 1)",
                "start_date": "string (ISO date)"
            },
            handler=self._create_recurring_task
        ))

        # Tool 2: Update Recurrence
        self.register_tool(MCPTool(
            name="update_recurrence",
            description="Update recurrence pattern for a task",
            parameters={
                "task_id": "int (required)",
                "pattern": "string",
                "interval": "int"
            },
            handler=self._update_recurrence
        ))

        # Tool 3: Stop Recurring
        self.register_tool(MCPTool(
            name="stop_recurring",
            description="Stop a recurring task series",
            parameters={"task_id": "int (required)"},
            handler=self._stop_recurring
        ))

        # Tool 4: Get Recurrence Patterns
        self.register_tool(MCPTool(
            name="get_recurrence_patterns",
            description="Get available recurrence patterns",
            parameters={},
            handler=self._get_patterns
        ))

        # Tool 5: Calculate Next Occurrence
        self.register_tool(MCPTool(
            name="calculate_next_occurrence",
            description="Calculate the next occurrence date",
            parameters={
                "pattern": "string (required)",
                "interval": "int (default: 1)",
                "from_date": "string (ISO date)"
            },
            handler=self._calculate_next
        ))

        # Tool 6: Get Recurring Series
        self.register_tool(MCPTool(
            name="get_recurring_series",
            description="Get all instances of a recurring task",
            parameters={"parent_task_id": "int (required)"},
            handler=self._get_series
        ))

        # Tool 7: Skip Occurrence
        self.register_tool(MCPTool(
            name="skip_occurrence",
            description="Skip the next occurrence of a recurring task",
            parameters={"task_id": "int (required)"},
            handler=self._skip_occurrence
        ))

        # Tool 8: Complete Recurring
        self.register_tool(MCPTool(
            name="complete_recurring",
            description="Complete recurring task and create next instance",
            parameters={"task_id": "int (required)"},
            handler=self._complete_recurring
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best Recurring tool"""
        query = query.lower()

        if any(w in query for w in ['create recurring', 'new recurring', 'repeat task', 'daily task', 'weekly task', 'monthly task']):
            return 'create_recurring_task'
        elif any(w in query for w in ['update recurrence', 'change pattern', 'modify recurring']):
            return 'update_recurrence'
        elif any(w in query for w in ['stop recurring', 'cancel recurring', 'end recurring']):
            return 'stop_recurring'
        elif any(w in query for w in ['pattern', 'recurrence option', 'recurring option']):
            return 'get_recurrence_patterns'
        elif any(w in query for w in ['next occurrence', 'next date', 'calculate next']):
            return 'calculate_next_occurrence'
        elif any(w in query for w in ['series', 'all instance', 'recurring instance']):
            return 'get_recurring_series'
        elif any(w in query for w in ['skip', 'skip occurrence']):
            return 'skip_occurrence'
        elif any(w in query for w in ['complete recurring', 'done recurring']):
            return 'complete_recurring'

        return 'get_recurrence_patterns'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'create_recurring_task':
            pattern = self._extract_pattern(query)
            return await self._create_recurring_task(
                user_id="user",
                title="Recurring Task",
                pattern=pattern
            )

        elif tool_name == 'update_recurrence':
            return await self._update_recurrence(task_id=1, pattern="weekly")

        elif tool_name == 'stop_recurring':
            return await self._stop_recurring(task_id=1)

        elif tool_name == 'get_recurrence_patterns':
            return await self._get_patterns()

        elif tool_name == 'calculate_next_occurrence':
            pattern = self._extract_pattern(query)
            return await self._calculate_next(pattern=pattern)

        elif tool_name == 'get_recurring_series':
            return await self._get_series(parent_task_id=1)

        elif tool_name == 'skip_occurrence':
            return await self._skip_occurrence(task_id=1)

        elif tool_name == 'complete_recurring':
            return await self._complete_recurring(task_id=1)

        else:
            return await self._get_patterns()

    def _extract_pattern(self, query: str) -> str:
        """Extract recurrence pattern from query"""
        if 'daily' in query or 'every day' in query:
            return 'daily'
        elif 'weekly' in query or 'every week' in query:
            return 'weekly'
        elif 'monthly' in query or 'every month' in query:
            return 'monthly'
        return 'weekly'

    def _calculate_next_date(self, pattern: str, interval: int,
                            from_date: datetime = None) -> datetime:
        """Calculate the next occurrence date"""
        from_date = from_date or datetime.utcnow()

        if pattern == 'daily':
            return from_date + timedelta(days=interval)
        elif pattern == 'weekly':
            return from_date + timedelta(weeks=interval)
        elif pattern == 'monthly':
            # Simple month calculation
            month = from_date.month + interval
            year = from_date.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            day = min(from_date.day, 28)  # Safe for all months
            return from_date.replace(year=year, month=month, day=day)
        else:
            return from_date + timedelta(days=interval)

    # ==================== Tool Handlers ====================

    async def _create_recurring_task(self, user_id: str, title: str,
                                     pattern: str = "weekly",
                                     interval: int = 1,
                                     start_date: str = None) -> Dict:
        """Create a recurring task"""
        if pattern not in self.patterns:
            return {
                "status": "error",
                "message": f"Invalid pattern. Use: {list(self.patterns.keys())}"
            }

        start = datetime.fromisoformat(start_date) if start_date else datetime.utcnow()
        next_occurrence = self._calculate_next_date(pattern, interval, start)

        return {
            "status": "success",
            "task": {
                "title": title,
                "is_recurring": True,
                "recurrence_pattern": pattern,
                "recurrence_interval": interval,
                "start_date": start.isoformat(),
                "next_occurrence": next_occurrence.isoformat()
            },
            "api_call": f"POST /api/{user_id}/tasks",
            "body": {
                "title": title,
                "is_recurring": True,
                "recurrence_pattern": pattern,
                "recurrence_interval": interval
            },
            "kafka_event": {
                "topic": "task-events",
                "event_type": "recurring_task_created",
                "pattern": pattern,
                "interval": interval
            },
            "mcp_tool_code": """
@tool
async def create_recurring_task(
    user_id: str,
    title: str,
    pattern: str,
    interval: int = 1
):
    task = Task(
        user_id=user_id,
        title=title,
        is_recurring=True,
        recurrence_pattern=pattern,
        recurrence_interval=interval,
        next_occurrence=calculate_next(pattern, interval)
    )
    await save_task(task)

    # Publish event for recurring task engine
    await publish_event("task-events", {
        "event_type": "recurring_task_created",
        "task_id": task.id,
        "pattern": pattern
    })

    return {"task_id": task.id, "next_occurrence": task.next_occurrence}
"""
        }

    async def _update_recurrence(self, task_id: int, pattern: str = None,
                                interval: int = None) -> Dict:
        """Update recurrence pattern"""
        return {
            "status": "success",
            "task_id": task_id,
            "updated": {
                "pattern": pattern,
                "interval": interval
            },
            "api_call": f"PATCH /api/user/tasks/{task_id}",
            "body": {
                "recurrence_pattern": pattern,
                "recurrence_interval": interval
            }
        }

    async def _stop_recurring(self, task_id: int) -> Dict:
        """Stop recurring task series"""
        return {
            "status": "success",
            "task_id": task_id,
            "action": "recurring_stopped",
            "api_call": f"PATCH /api/user/tasks/{task_id}",
            "body": {"is_recurring": False},
            "note": "Future occurrences will not be created"
        }

    async def _get_patterns(self) -> Dict:
        """Get available recurrence patterns"""
        return {
            "status": "success",
            "patterns": [
                {
                    "name": "daily",
                    "description": "Repeats every N days",
                    "examples": ["Every day", "Every 2 days", "Every 3 days"]
                },
                {
                    "name": "weekly",
                    "description": "Repeats every N weeks",
                    "examples": ["Every week", "Every 2 weeks", "Bi-weekly"]
                },
                {
                    "name": "monthly",
                    "description": "Repeats every N months",
                    "examples": ["Every month", "Every 2 months", "Quarterly"]
                },
                {
                    "name": "custom",
                    "description": "Custom interval in days",
                    "examples": ["Every 5 days", "Every 10 days"]
                }
            ],
            "usage": "create_recurring_task(title='Meeting', pattern='weekly', interval=1)"
        }

    async def _calculate_next(self, pattern: str, interval: int = 1,
                             from_date: str = None) -> Dict:
        """Calculate next occurrence"""
        base_date = datetime.fromisoformat(from_date) if from_date else datetime.utcnow()
        next_date = self._calculate_next_date(pattern, interval, base_date)

        return {
            "status": "success",
            "from_date": base_date.isoformat(),
            "pattern": pattern,
            "interval": interval,
            "next_occurrence": next_date.isoformat(),
            "days_until": (next_date - base_date).days
        }

    async def _get_series(self, parent_task_id: int) -> Dict:
        """Get all instances of recurring task"""
        return {
            "status": "success",
            "parent_task_id": parent_task_id,
            "api_call": f"GET /api/user/tasks?parent_task_id={parent_task_id}",
            "sql_query": f"""
SELECT * FROM tasks
WHERE parent_task_id = {parent_task_id}
   OR id = {parent_task_id}
ORDER BY created_at ASC
""",
            "note": "Returns original task and all generated instances"
        }

    async def _skip_occurrence(self, task_id: int) -> Dict:
        """Skip next occurrence"""
        return {
            "status": "success",
            "task_id": task_id,
            "action": "occurrence_skipped",
            "api_call": f"POST /api/user/tasks/{task_id}/skip",
            "note": "Next occurrence will be skipped, following occurrence calculated"
        }

    async def _complete_recurring(self, task_id: int) -> Dict:
        """Complete recurring task and create next"""
        next_date = self._calculate_next_date("weekly", 1)

        return {
            "status": "success",
            "task_id": task_id,
            "action": "completed_and_next_created",
            "next_task": {
                "parent_task_id": task_id,
                "scheduled_for": next_date.isoformat()
            },
            "kafka_event": {
                "topic": "task-events",
                "event_type": "recurring_task_completed",
                "task_id": task_id,
                "next_occurrence": next_date.isoformat()
            },
            "flow": """
1. Mark current task as completed
2. Check if is_recurring = true
3. Calculate next occurrence date
4. Create new task instance with parent_task_id
5. Publish 'recurring_task_completed' event
6. Recurring Task Service consumes event and handles edge cases
"""
        }
