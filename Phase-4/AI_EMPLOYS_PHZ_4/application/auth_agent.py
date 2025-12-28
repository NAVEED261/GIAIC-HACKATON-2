"""
Auth Agent - Authentication & Authorization Expert
Handles login, signup, token management

@author: Phase-4 Multi-Agent System
"""

import asyncio
import aiohttp
from typing import Dict, Any
import sys
sys.path.append('..')
from base_agent import BaseAgent


class AuthAgent(BaseAgent):
    """
    Authentication Expert Agent
    Handles: login, signup, logout, token management
    """

    KEYWORDS = [
        'auth', 'login', 'signin', 'signup', 'register', 'logout',
        'token', 'password', 'user', 'credential', 'session'
    ]

    def __init__(self, api_url: str = "http://127.0.0.1:65525"):
        super().__init__("Auth", "Authentication & authorization expert")
        self.api_url = api_url
        self.current_token = None
        self.current_user = None

    def can_handle(self, task: str) -> bool:
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in self.KEYWORDS)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_str = task.get("task", "")
        params = task.get("params", {})

        self.start_work(task_str)

        try:
            if "signup" in task_str.lower() or "register" in task_str.lower():
                result = await self.signup(params)
            elif "login" in task_str.lower() or "signin" in task_str.lower():
                result = await self.login(params)
            elif "logout" in task_str.lower():
                result = await self.logout()
            elif "me" in task_str.lower() or "current" in task_str.lower():
                result = await self.get_current_user()
            elif "verify" in task_str.lower() or "check" in task_str.lower():
                result = await self.verify_token(params)
            else:
                result = {"status": "unknown auth action"}

            self.end_work("Task completed")
            return {"success": True, "data": result}

        except Exception as e:
            self.report_error(str(e))
            return {"success": False, "error": str(e)}

    async def signup(self, params: Dict) -> Dict:
        email = params.get("email")
        password = params.get("password")
        name = params.get("name", email.split("@")[0] if email else "User")

        self.log(f"Registering user: {email}", "working")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/api/auth/signup",
                json={"email": email, "password": password, "name": name}
            ) as resp:
                if resp.status == 201:
                    return await resp.json()
                error = await resp.text()
                raise Exception(f"Signup failed: {error}")

    async def login(self, params: Dict) -> Dict:
        email = params.get("email")
        password = params.get("password")

        self.log(f"Logging in: {email}", "working")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/api/auth/signin",
                json={"email": email, "password": password}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.current_token = data.get("access_token")
                    self.current_user = {
                        "id": data.get("user_id"),
                        "email": data.get("email"),
                        "name": data.get("name")
                    }
                    return data
                raise Exception("Invalid credentials")

    async def logout(self) -> Dict:
        self.log("Logging out", "working")
        self.current_token = None
        self.current_user = None
        return {"status": "logged out"}

    async def get_current_user(self) -> Dict:
        if not self.current_token:
            raise Exception("Not logged in")

        self.log("Getting current user", "working")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/auth/me",
                headers={"Authorization": f"Bearer {self.current_token}"}
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                raise Exception("Failed to get current user")

    async def verify_token(self, params: Dict) -> Dict:
        token = params.get("token", self.current_token)

        if not token:
            return {"valid": False, "reason": "No token provided"}

        self.log("Verifying token", "working")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/api/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            ) as resp:
                return {
                    "valid": resp.status == 200,
                    "status_code": resp.status
                }

    def get_token(self) -> str:
        return self.current_token

    def get_user(self) -> Dict:
        return self.current_user
