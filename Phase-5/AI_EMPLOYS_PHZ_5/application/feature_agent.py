"""
Feature Agent - Advanced Features Expert
Handles Priority, Tags, Search, Filter, Sort for Phase-5

@author: Phase-5 AI Employs System
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, MCPTool, AgentResult


class FeatureAgent(BaseAgent):
    """
    Advanced Features Expert Agent

    Capabilities:
    - Priority management (high, medium, low)
    - Tags/Categories management
    - Search functionality
    - Filter functionality
    - Sort functionality

    MCP Tools: 12
    """

    def __init__(self):
        super().__init__()
        self.name = "FeatureAgent"
        self.domain = "feature"
        self.description = "Advanced features expert (Priority, Tags, Search, Filter, Sort)"
        self.emoji = "⚡"

        # Priority levels
        self.priorities = {
            "high": {"color": "red", "emoji": "🔴", "order": 1},
            "medium": {"color": "yellow", "emoji": "🟡", "order": 2},
            "low": {"color": "green", "emoji": "🟢", "order": 3}
        }

        # Default tags
        self.default_tags = ["work", "home", "urgent", "shopping", "personal"]

    def _setup_tools(self):
        """Setup Feature MCP tools"""

        # Tool 1: Set Priority
        self.register_tool(MCPTool(
            name="set_priority",
            description="Set task priority (high, medium, low)",
            parameters={
                "task_id": "int (required)",
                "priority": "string (high/medium/low)"
            },
            handler=self._set_priority
        ))

        # Tool 2: Get Priorities
        self.register_tool(MCPTool(
            name="get_priorities",
            description="Get available priority levels",
            parameters={},
            handler=self._get_priorities
        ))

        # Tool 3: Add Tags
        self.register_tool(MCPTool(
            name="add_tags",
            description="Add tags to a task",
            parameters={
                "task_id": "int (required)",
                "tags": "list[string] (required)"
            },
            handler=self._add_tags
        ))

        # Tool 4: Remove Tags
        self.register_tool(MCPTool(
            name="remove_tags",
            description="Remove tags from a task",
            parameters={
                "task_id": "int (required)",
                "tags": "list[string] (required)"
            },
            handler=self._remove_tags
        ))

        # Tool 5: List Tags
        self.register_tool(MCPTool(
            name="list_tags",
            description="List all available tags",
            parameters={"user_id": "string (optional)"},
            handler=self._list_tags
        ))

        # Tool 6: Create Tag
        self.register_tool(MCPTool(
            name="create_tag",
            description="Create a new custom tag",
            parameters={
                "name": "string (required)",
                "color": "string (optional)"
            },
            handler=self._create_tag
        ))

        # Tool 7: Search Tasks
        self.register_tool(MCPTool(
            name="search_tasks",
            description="Search tasks by keyword",
            parameters={
                "user_id": "string (required)",
                "query": "string (required)"
            },
            handler=self._search_tasks
        ))

        # Tool 8: Filter Tasks
        self.register_tool(MCPTool(
            name="filter_tasks",
            description="Filter tasks by criteria",
            parameters={
                "user_id": "string (required)",
                "status": "string (all/pending/completed)",
                "priority": "string (high/medium/low)",
                "tags": "list[string]",
                "due_from": "string (ISO date)",
                "due_to": "string (ISO date)"
            },
            handler=self._filter_tasks
        ))

        # Tool 9: Sort Tasks
        self.register_tool(MCPTool(
            name="sort_tasks",
            description="Sort tasks by field",
            parameters={
                "sort_by": "string (due_date/priority/title/created_at)",
                "order": "string (asc/desc)"
            },
            handler=self._sort_tasks
        ))

        # Tool 10: Get Filter Options
        self.register_tool(MCPTool(
            name="get_filter_options",
            description="Get available filter options",
            parameters={},
            handler=self._get_filter_options
        ))

        # Tool 11: Get Sort Options
        self.register_tool(MCPTool(
            name="get_sort_options",
            description="Get available sort options",
            parameters={},
            handler=self._get_sort_options
        ))

        # Tool 12: Advanced Query
        self.register_tool(MCPTool(
            name="advanced_query",
            description="Combined search, filter, and sort",
            parameters={
                "user_id": "string (required)",
                "search": "string (optional)",
                "filters": "dict (optional)",
                "sort": "dict (optional)"
            },
            handler=self._advanced_query
        ))

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best Feature tool"""
        query = query.lower()

        if any(w in query for w in ['set priority', 'change priority', 'priority to']):
            return 'set_priority'
        elif any(w in query for w in ['priority option', 'priority level', 'what priorit']):
            return 'get_priorities'
        elif any(w in query for w in ['add tag', 'tag task', 'label']):
            return 'add_tags'
        elif any(w in query for w in ['remove tag', 'delete tag', 'untag']):
            return 'remove_tags'
        elif any(w in query for w in ['list tag', 'show tag', 'all tag']):
            return 'list_tags'
        elif any(w in query for w in ['create tag', 'new tag']):
            return 'create_tag'
        elif any(w in query for w in ['search', 'find', 'look for']):
            return 'search_tasks'
        elif any(w in query for w in ['filter', 'show only', 'show me']):
            return 'filter_tasks'
        elif any(w in query for w in ['sort', 'order by', 'arrange']):
            return 'sort_tasks'
        elif any(w in query for w in ['filter option']):
            return 'get_filter_options'
        elif any(w in query for w in ['sort option']):
            return 'get_sort_options'
        elif any(w in query for w in ['advanced', 'complex query']):
            return 'advanced_query'

        return 'get_filter_options'

    async def execute_direct(self, step: Dict) -> Any:
        """Smart direct execution"""
        query = step.get("query", "").lower()
        tool_name = step.get("tool") or self._match_tool(query)

        if tool_name == 'set_priority':
            # Extract priority from query
            priority = self._extract_priority(query)
            return await self._set_priority(task_id=1, priority=priority)

        elif tool_name == 'get_priorities':
            return await self._get_priorities()

        elif tool_name == 'add_tags':
            tags = self._extract_tags(query)
            return await self._add_tags(task_id=1, tags=tags)

        elif tool_name == 'remove_tags':
            tags = self._extract_tags(query)
            return await self._remove_tags(task_id=1, tags=tags)

        elif tool_name == 'list_tags':
            return await self._list_tags()

        elif tool_name == 'create_tag':
            name = self._extract_tag_name(query)
            return await self._create_tag(name=name or "custom")

        elif tool_name == 'search_tasks':
            keyword = self._extract_search_keyword(query)
            return await self._search_tasks(user_id="user", query=keyword)

        elif tool_name == 'filter_tasks':
            return await self._filter_tasks(user_id="user")

        elif tool_name == 'sort_tasks':
            sort_by = self._extract_sort_field(query)
            return await self._sort_tasks(sort_by=sort_by)

        elif tool_name == 'get_filter_options':
            return await self._get_filter_options()

        elif tool_name == 'get_sort_options':
            return await self._get_sort_options()

        elif tool_name == 'advanced_query':
            return await self._advanced_query(user_id="user")

        else:
            return await self._get_filter_options()

    def _extract_priority(self, query: str) -> str:
        """Extract priority from query"""
        if 'high' in query:
            return 'high'
        elif 'low' in query:
            return 'low'
        return 'medium'

    def _extract_tags(self, query: str) -> List[str]:
        """Extract tags from query"""
        tags = []
        for tag in self.default_tags:
            if tag in query.lower():
                tags.append(tag)
        return tags or ['work']

    def _extract_tag_name(self, query: str) -> Optional[str]:
        """Extract tag name from query"""
        words = query.split()
        for i, word in enumerate(words):
            if word in ['tag', 'label'] and i + 1 < len(words):
                return words[i + 1]
        return None

    def _extract_search_keyword(self, query: str) -> str:
        """Extract search keyword from query"""
        # Remove common words
        stop_words = ['search', 'find', 'look', 'for', 'task', 'tasks']
        words = [w for w in query.split() if w.lower() not in stop_words]
        return ' '.join(words) or 'meeting'

    def _extract_sort_field(self, query: str) -> str:
        """Extract sort field from query"""
        if 'due' in query or 'date' in query:
            return 'due_date'
        elif 'priority' in query:
            return 'priority'
        elif 'alpha' in query or 'name' in query or 'title' in query:
            return 'title'
        return 'created_at'

    # ==================== Tool Handlers ====================

    async def _set_priority(self, task_id: int, priority: str) -> Dict:
        """Set task priority"""
        if priority not in self.priorities:
            return {
                "status": "error",
                "message": f"Invalid priority. Use: {list(self.priorities.keys())}"
            }

        priority_info = self.priorities[priority]

        return {
            "status": "success",
            "task_id": task_id,
            "priority": priority,
            "color": priority_info["color"],
            "emoji": priority_info["emoji"],
            "api_call": f"PATCH /api/user/tasks/{task_id}",
            "body": {"priority": priority},
            "mcp_tool_code": f"""
@tool
async def set_priority(user_id: str, task_id: int, priority: str):
    task = await get_task(user_id, task_id)
    task.priority = priority
    await save_task(task)
    return {{"task_id": task_id, "priority": priority}}
"""
        }

    async def _get_priorities(self) -> Dict:
        """Get available priorities"""
        return {
            "status": "success",
            "priorities": [
                {
                    "level": level,
                    "color": info["color"],
                    "emoji": info["emoji"],
                    "sort_order": info["order"]
                }
                for level, info in self.priorities.items()
            ],
            "usage": "set_priority(task_id=1, priority='high')"
        }

    async def _add_tags(self, task_id: int, tags: List[str]) -> Dict:
        """Add tags to task"""
        return {
            "status": "success",
            "task_id": task_id,
            "tags_added": tags,
            "api_call": f"PATCH /api/user/tasks/{task_id}",
            "body": {"tags": {"add": tags}},
            "mcp_tool_code": f"""
@tool
async def add_tags(user_id: str, task_id: int, tags: List[str]):
    task = await get_task(user_id, task_id)
    task.tags = list(set(task.tags + tags))
    await save_task(task)
    return {{"task_id": task_id, "tags": task.tags}}
"""
        }

    async def _remove_tags(self, task_id: int, tags: List[str]) -> Dict:
        """Remove tags from task"""
        return {
            "status": "success",
            "task_id": task_id,
            "tags_removed": tags,
            "api_call": f"PATCH /api/user/tasks/{task_id}",
            "body": {"tags": {"remove": tags}}
        }

    async def _list_tags(self, user_id: str = None) -> Dict:
        """List all tags"""
        return {
            "status": "success",
            "default_tags": self.default_tags,
            "tag_colors": {
                "work": "blue",
                "home": "green",
                "urgent": "red",
                "shopping": "purple",
                "personal": "orange"
            },
            "api_call": "GET /api/user/tags"
        }

    async def _create_tag(self, name: str, color: str = "gray") -> Dict:
        """Create a new tag"""
        return {
            "status": "success",
            "tag": {"name": name, "color": color},
            "api_call": "POST /api/user/tags",
            "body": {"name": name, "color": color}
        }

    async def _search_tasks(self, user_id: str, query: str) -> Dict:
        """Search tasks by keyword"""
        return {
            "status": "success",
            "search_query": query,
            "api_call": f"GET /api/{user_id}/tasks/search?q={query}",
            "sql_query": f"""
SELECT * FROM tasks
WHERE user_id = '{user_id}'
AND (
    title ILIKE '%{query}%'
    OR description ILIKE '%{query}%'
)
ORDER BY created_at DESC
""",
            "mcp_tool_code": f"""
@tool
async def search_tasks(user_id: str, query: str):
    tasks = await db.query(
        "SELECT * FROM tasks WHERE user_id = $1 AND (title ILIKE $2 OR description ILIKE $2)",
        user_id, f"%{{query}}%"
    )
    return {{"results": tasks, "count": len(tasks)}}
"""
        }

    async def _filter_tasks(self, user_id: str, status: str = "all",
                           priority: str = None, tags: List[str] = None,
                           due_from: str = None, due_to: str = None) -> Dict:
        """Filter tasks"""
        filters = {}
        if status != "all":
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if tags:
            filters["tags"] = tags
        if due_from:
            filters["due_from"] = due_from
        if due_to:
            filters["due_to"] = due_to

        query_params = "&".join([f"{k}={v}" for k, v in filters.items()])

        return {
            "status": "success",
            "filters_applied": filters,
            "api_call": f"GET /api/{user_id}/tasks?{query_params}",
            "mcp_tool_code": """
@tool
async def filter_tasks(
    user_id: str,
    status: str = "all",
    priority: str = None,
    tags: List[str] = None,
    due_from: str = None,
    due_to: str = None
):
    query = "SELECT * FROM tasks WHERE user_id = $1"
    params = [user_id]

    if status != "all":
        query += f" AND completed = ${len(params) + 1}"
        params.append(status == "completed")

    if priority:
        query += f" AND priority = ${len(params) + 1}"
        params.append(priority)

    # ... more filters

    return await db.query(query, *params)
"""
        }

    async def _sort_tasks(self, sort_by: str = "created_at",
                         order: str = "desc") -> Dict:
        """Sort tasks"""
        valid_fields = ["due_date", "priority", "title", "created_at", "updated_at"]

        if sort_by not in valid_fields:
            return {
                "status": "error",
                "message": f"Invalid sort field. Use: {valid_fields}"
            }

        return {
            "status": "success",
            "sort_by": sort_by,
            "order": order,
            "api_call": f"GET /api/user/tasks?sort={sort_by}&order={order}",
            "sql_order": f"ORDER BY {sort_by} {order.upper()}"
        }

    async def _get_filter_options(self) -> Dict:
        """Get available filter options"""
        return {
            "status": "success",
            "filter_options": {
                "status": ["all", "pending", "completed"],
                "priority": ["high", "medium", "low"],
                "tags": self.default_tags,
                "date_range": {
                    "due_from": "ISO date string",
                    "due_to": "ISO date string"
                }
            },
            "example": "GET /api/user/tasks?status=pending&priority=high&tags=work"
        }

    async def _get_sort_options(self) -> Dict:
        """Get available sort options"""
        return {
            "status": "success",
            "sort_options": {
                "fields": ["due_date", "priority", "title", "created_at", "updated_at"],
                "orders": ["asc", "desc"]
            },
            "example": "GET /api/user/tasks?sort=due_date&order=asc"
        }

    async def _advanced_query(self, user_id: str, search: str = None,
                             filters: Dict = None, sort: Dict = None) -> Dict:
        """Combined advanced query"""
        return {
            "status": "success",
            "query_type": "advanced",
            "parameters": {
                "search": search,
                "filters": filters or {},
                "sort": sort or {"by": "created_at", "order": "desc"}
            },
            "example_natural_language": [
                "Show me high priority work tasks due this week sorted by due date",
                "Find all pending tasks tagged urgent",
                "Search for 'meeting' in completed tasks"
            ],
            "api_example": "GET /api/user/tasks?q=meeting&status=pending&priority=high&tags=work&sort=due_date&order=asc"
        }
