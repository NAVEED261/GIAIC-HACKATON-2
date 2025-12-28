"""
Task Agent - Todo Task Management Expert
Handles all task CRUD operations via API

@author: Phase-4 Multi-Agent System
"""

import asyncio
import aiohttp
from typing import Dict, Any, List
import sys
sys.path.append('..')
from base_agent import BaseAgent


class TaskAgent(BaseAgent):
    """
    Task Management Expert Agent
    Handles: create, read, update, delete tasks
    """

    KEYWORDS = [
        'task', 'todo', 'add', 'create', 'list', 'show', 'complete',
        'done', 'delete', 'remove', 'update', 'edit', 'mark'
    ]

    def __init__(self, api_url: str = "http://127.0.0.1:65525"):
        super().__init__("Task", "Todo task management expert")
        self.api_url = api_url
        self.token = None

    def set_token(self, token: str):
        """Set auth token for API calls"""
        self.token = token

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_str = task.get("task", "")
        params = task.get("params", {})

        self.start_work(task_str)

        try:
            if "add" in task_str.lower() or "create" in task_str.lower():
                result = await self.create_task(params)
            elif "list" in task_str.lower() or "show" in task_str.lower():
                result = await self.list_tasks(params)
            elif "complete" in task_str.lower() or "done" in task_str.lower():
                result = await self.complete_task(params)
            elif "delete" in task_str.lower() or "remove" in task_str.lower():
                result = await self.delete_task(params)
            elif "update" in task_str.lower() or "edit" in task_str.lower():
                result = await self.update_task(params)
            else:
                result = await self.list_tasks(params)

            self.end_work("Task completed")
            return {"success": True, "data": result}

        except Exception as e:
            self.report_error(str(e))
            return {"success": False, "error": str(e)}

    def _headers(self) -> Dict:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def create_task(self, params: Dict) -> Dict:
        title = params.get("title", "New Task")
        description = params.get("description", "")
        user_id = params.get("user_id", 1)

        self.log(f"Creating task: {title}", "working")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/api/{user_id}/tasks",
                json={"title": title, "description": description},
                headers=self._headers()
            ) as resp:
                if resp.status == 201:
                    return await resp.json()
                raise Exception(f"Failed to create task: {resp.status}")

    async def list_tasks(self, params: Dict) -> List[Dict]:
        user_id = params.get("user_id", 1)
        status = params.get("status", "all")

        self.log(f"Listing tasks (status: {status})", "working")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/{user_id}/tasks",
                params={"status": status},
                headers=self._headers()
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise Exception(f"Failed to list tasks: {resp.status}")

    async def complete_task(self, params: Dict) -> Dict:
        task_id = params.get("task_id", params.get("id"))
        user_id = params.get("user_id", 1)

        self.log(f"Completing task {task_id}", "working")

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{self.api_url}/api/{user_id}/tasks/{task_id}/complete",
                headers=self._headers()
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise Exception(f"Failed to complete task: {resp.status}")

    async def delete_task(self, params: Dict) -> Dict:
        task_id = params.get("task_id", params.get("id"))
        user_id = params.get("user_id", 1)

        self.log(f"Deleting task {task_id}", "working")

        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.api_url}/api/{user_id}/tasks/{task_id}",
                headers=self._headers()
            ) as resp:
                if resp.status == 200:
                    return {"deleted": True, "task_id": task_id}
                raise Exception(f"Failed to delete task: {resp.status}")

    async def update_task(self, params: Dict) -> Dict:
        task_id = params.get("task_id", params.get("id"))
        user_id = params.get("user_id", 1)
        title = params.get("title")
        description = params.get("description")

        self.log(f"Updating task {task_id}", "working")

        update_data = {}
        if title:
            update_data["title"] = title
        if description:
            update_data["description"] = description

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{self.api_url}/api/{user_id}/tasks/{task_id}",
                json=update_data,
                headers=self._headers()
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise Exception(f"Failed to update task: {resp.status}")
