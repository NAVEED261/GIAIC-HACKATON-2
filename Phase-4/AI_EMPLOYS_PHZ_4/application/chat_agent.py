"""
Chat Agent - AI Conversation Expert
Handles chat interactions and AI responses

@author: Phase-4 Multi-Agent System
"""

import asyncio
import aiohttp
from typing import Dict, Any, List
import sys
sys.path.append('..')
from base_agent import BaseAgent


class ChatAgent(BaseAgent):
    """
    Chat/AI Expert Agent
    Handles: chat messages, conversations, AI responses
    """

    KEYWORDS = [
        'chat', 'message', 'conversation', 'talk', 'ask', 'ai',
        'response', 'history', 'say', 'tell'
    ]

    def __init__(self, api_url: str = "http://127.0.0.1:65525"):
        super().__init__("Chat", "AI conversation expert")
        self.api_url = api_url
        self.token = None
        self.conversation_id = None

    def set_token(self, token: str):
        self.token = token

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_str = task.get("task", "")
        params = task.get("params", {})

        self.start_work(task_str)

        try:
            if "history" in task_str.lower() or "conversations" in task_str.lower():
                result = await self.get_conversations(params)
            elif "send" in task_str.lower() or "message" in task_str.lower():
                result = await self.send_message(params)
            else:
                # Default: send as chat message
                result = await self.send_message({"message": task_str, **params})

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

    async def send_message(self, params: Dict) -> Dict:
        message = params.get("message", "")
        user_id = params.get("user_id", 1)
        conversation_id = params.get("conversation_id", self.conversation_id)

        self.log(f"Sending message: {message[:50]}...", "working")

        async with aiohttp.ClientSession() as session:
            payload = {"message": message}
            if conversation_id:
                payload["conversation_id"] = conversation_id

            async with session.post(
                f"{self.api_url}/api/{user_id}/chat",
                json=payload,
                headers=self._headers()
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.conversation_id = data.get("conversation_id")
                    return data
                raise Exception(f"Chat failed: {resp.status}")

    async def get_conversations(self, params: Dict) -> List[Dict]:
        user_id = params.get("user_id", 1)

        self.log("Getting conversation history", "working")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/{user_id}/conversations",
                headers=self._headers()
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise Exception(f"Failed to get conversations: {resp.status}")

    async def get_messages(self, params: Dict) -> List[Dict]:
        user_id = params.get("user_id", 1)
        conversation_id = params.get("conversation_id", self.conversation_id)

        self.log(f"Getting messages for conversation {conversation_id}", "working")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/{user_id}/conversations/{conversation_id}",
                headers=self._headers()
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise Exception(f"Failed to get messages: {resp.status}")
