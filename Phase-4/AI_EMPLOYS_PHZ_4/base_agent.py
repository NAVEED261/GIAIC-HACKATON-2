"""
Base Agent - POWERFUL Foundation with MCP Tools & Self-Reasoning
Capable of handling complex queries autonomously

@author: Phase-4 Multi-Agent System
"""

import os
import time
import json
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from colorama import Fore, Style, init
from openai import OpenAI

# Initialize colorama for Windows
init()


class MCPTool:
    """MCP Tool wrapper for agents"""

    def __init__(self, name: str, description: str, parameters: Dict, handler: Callable):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.handler = handler

    def to_openai_function(self) -> Dict:
        """Convert to OpenAI function format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    async def execute(self, **kwargs) -> Any:
        """Execute the tool"""
        if asyncio.iscoroutinefunction(self.handler):
            return await self.handler(**kwargs)
        return self.handler(**kwargs)


class BaseAgent(ABC):
    """
    POWERFUL Base Agent with:
    - MCP Tools integration
    - Self-reasoning with OpenAI
    - Multi-step execution
    - Tool chaining
    - Error recovery
    """

    COLORS = {
        'orchestrator': Fore.YELLOW,
        'docker': Fore.BLUE,
        'kubernetes': Fore.CYAN,
        'helm': Fore.MAGENTA,
        'network': Fore.GREEN,
        'task': Fore.WHITE,
        'chat': Fore.LIGHTBLUE_EX,
        'auth': Fore.LIGHTRED_EX,
        'database': Fore.LIGHTGREEN_EX,
        'cicd': Fore.LIGHTYELLOW_EX,
        'monitoring': Fore.LIGHTMAGENTA_EX,
        'security': Fore.RED,
        'backup': Fore.LIGHTCYAN_EX,
        'architect': Fore.LIGHTWHITE_EX,
        'debugger': Fore.LIGHTYELLOW_EX,
        'optimizer': Fore.LIGHTGREEN_EX,
    }

    EMOJIS = {
        'orchestrator': '🎯',
        'docker': '🐳',
        'kubernetes': '☸️',
        'helm': '⛵',
        'network': '🌐',
        'task': '📝',
        'chat': '💬',
        'auth': '🔐',
        'database': '🗄️',
        'cicd': '🔄',
        'monitoring': '📊',
        'security': '🛡️',
        'backup': '💾',
        'architect': '🏗️',
        'debugger': '🔧',
        'optimizer': '⚡',
    }

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.color = self.COLORS.get(name.lower(), Fore.WHITE)
        self.emoji = self.EMOJIS.get(name.lower(), '🤖')
        self.start_time = None
        self.is_working = False

        # MCP Tools registry
        self.tools: Dict[str, MCPTool] = {}

        # OpenAI client for reasoning
        self.client = None
        self._init_openai()

        # Execution history for learning
        self.execution_history: List[Dict] = []

        # Max retries for error recovery
        self.max_retries = 3

    def _init_openai(self):
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)

    # ==================== LOGGING ====================

    def log(self, message: str, level: str = "info"):
        """Log with visibility"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"{self.color}{self.emoji} [{self.name}]{Style.RESET_ALL}"

        if level == "start":
            print(f"\n{prefix} {Fore.GREEN}▶ Starting...{Style.RESET_ALL}")
            print(f"   └─ {message}")
        elif level == "working":
            print(f"{prefix} {Fore.YELLOW}⚙️ {Style.RESET_ALL} {message}")
        elif level == "tool":
            print(f"{prefix} {Fore.CYAN}🔧 Tool:{Style.RESET_ALL} {message}")
        elif level == "thinking":
            print(f"{prefix} {Fore.MAGENTA}🧠 Thinking:{Style.RESET_ALL} {message}")
        elif level == "step":
            print(f"{prefix} {Fore.BLUE}📍 Step:{Style.RESET_ALL} {message}")
        elif level == "success":
            print(f"{prefix} {Fore.GREEN}✅ Done:{Style.RESET_ALL} {message}")
        elif level == "error":
            print(f"{prefix} {Fore.RED}❌ Error:{Style.RESET_ALL} {message}")
        elif level == "retry":
            print(f"{prefix} {Fore.YELLOW}🔄 Retry:{Style.RESET_ALL} {message}")
        elif level == "delegate":
            print(f"{prefix} {Fore.CYAN}➡️ Delegating:{Style.RESET_ALL} {message}")
        else:
            print(f"{prefix} {message}")

    def start_work(self, task: str):
        self.is_working = True
        self.start_time = time.time()
        self.log(task, "start")

    def end_work(self, result: str):
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.is_working = False
        self.log(f"{result} ({elapsed:.2f}s)", "success")

    def report_error(self, error: str):
        self.is_working = False
        self.log(error, "error")

    # ==================== MCP TOOLS ====================

    def register_tool(self, tool: MCPTool):
        """Register an MCP tool"""
        self.tools[tool.name] = tool
        self.log(f"Registered tool: {tool.name}", "tool")

    def register_tools(self, tools: List[MCPTool]):
        """Register multiple tools"""
        for tool in tools:
            self.register_tool(tool)

    def get_openai_tools(self) -> List[Dict]:
        """Get all tools in OpenAI format"""
        return [tool.to_openai_function() for tool in self.tools.values()]

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")

        tool = self.tools[tool_name]
        self.log(f"{tool_name}({json.dumps(kwargs)[:50]}...)", "tool")

        try:
            result = await tool.execute(**kwargs)
            return result
        except Exception as e:
            self.log(f"Tool {tool_name} failed: {e}", "error")
            raise

    # ==================== SELF-REASONING ====================

    async def reason(self, query: str, context: Dict = None) -> Dict:
        """
        Use AI to reason about how to solve the query.
        Returns a plan with steps.
        """
        if not self.client:
            return {"steps": [{"action": "direct", "query": query}]}

        self.log("Analyzing query...", "thinking")

        system_prompt = f"""You are {self.name} Agent - {self.description}.

Available tools:
{json.dumps([t.to_openai_function() for t in self.tools.values()], indent=2)}

Given a query, create a step-by-step plan to solve it.
Each step should use one of the available tools.

Respond with JSON:
{{
    "understanding": "what the user wants",
    "steps": [
        {{"tool": "tool_name", "params": {{}}, "reason": "why this step"}}
    ],
    "expected_outcome": "what result to expect"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}\nContext: {json.dumps(context or {})}"}
                ],
                response_format={"type": "json_object"}
            )

            plan = json.loads(response.choices[0].message.content)
            self.log(f"Plan: {len(plan.get('steps', []))} steps", "thinking")
            return plan

        except Exception as e:
            self.log(f"Reasoning failed: {e}", "error")
            return {"steps": [{"action": "direct", "query": query}]}

    # ==================== MULTI-STEP EXECUTION ====================

    async def execute_plan(self, plan: Dict) -> Dict:
        """Execute a multi-step plan"""
        results = []
        context = {}

        steps = plan.get("steps", [])
        total = len(steps)

        for i, step in enumerate(steps, 1):
            self.log(f"[{i}/{total}] {step.get('reason', step.get('tool', 'action'))}", "step")

            tool_name = step.get("tool")
            params = step.get("params", {})

            # Inject context from previous steps
            params["_context"] = context

            try:
                if tool_name and tool_name in self.tools:
                    result = await self.execute_tool(tool_name, **params)
                else:
                    # Direct execution
                    result = await self.execute_direct(step)

                results.append({"step": i, "tool": tool_name, "result": result})
                context[f"step_{i}"] = result

            except Exception as e:
                results.append({"step": i, "tool": tool_name, "error": str(e)})

                # Try to recover
                if not await self.try_recover(step, e, context):
                    break

        return {
            "plan": plan,
            "results": results,
            "final_context": context
        }

    async def execute_direct(self, step: Dict) -> Any:
        """Execute a step directly (override in subclass)"""
        return {"status": "executed", "step": step}

    # ==================== ERROR RECOVERY ====================

    async def try_recover(self, failed_step: Dict, error: Exception, context: Dict) -> bool:
        """Try to recover from a failed step"""
        self.log(f"Attempting recovery from: {error}", "retry")

        for attempt in range(self.max_retries):
            self.log(f"Retry {attempt + 1}/{self.max_retries}", "retry")

            try:
                # Ask AI for recovery strategy
                if self.client:
                    recovery = await self.get_recovery_strategy(failed_step, error, context)
                    if recovery.get("skip"):
                        return True
                    if recovery.get("alternative_step"):
                        await self.execute_plan({"steps": [recovery["alternative_step"]]})
                        return True

                # Simple retry
                await asyncio.sleep(1)
                tool_name = failed_step.get("tool")
                if tool_name:
                    await self.execute_tool(tool_name, **failed_step.get("params", {}))
                    return True

            except Exception:
                continue

        return False

    async def get_recovery_strategy(self, step: Dict, error: Exception, context: Dict) -> Dict:
        """Get AI-powered recovery strategy"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You help recover from failed operations. Respond with JSON."},
                    {"role": "user", "content": f"Step failed: {step}\nError: {error}\nContext: {context}\n\nHow to recover?"}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except:
            return {}

    # ==================== MAIN EXECUTION ====================

    async def process(self, query: str, params: Dict = None) -> Dict:
        """
        MAIN ENTRY POINT - Process any query with full power:
        1. Reason about the query
        2. Create execution plan
        3. Execute multi-step plan
        4. Recover from errors
        5. Return results
        """
        self.start_work(query)

        try:
            # Step 1: Reason and plan
            plan = await self.reason(query, params)

            # Step 2: Execute plan
            result = await self.execute_plan(plan)

            # Step 3: Store in history
            self.execution_history.append({
                "query": query,
                "plan": plan,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })

            self.end_work("Query processed successfully")
            return {"success": True, "data": result}

        except Exception as e:
            self.report_error(str(e))
            return {"success": False, "error": str(e)}

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task - implement in subclass"""
        pass

    @abstractmethod
    def can_handle(self, task: str) -> bool:
        """Check if can handle task - implement in subclass"""
        pass

    # ==================== UTILITIES ====================

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "emoji": self.emoji,
            "description": self.description,
            "is_working": self.is_working,
            "tools_count": len(self.tools),
            "tools": list(self.tools.keys()),
            "history_count": len(self.execution_history)
        }


class AgentResult:
    """Standard result format"""

    def __init__(self, success: bool, data: Any = None, error: str = None, agent: str = None):
        self.success = success
        self.data = data
        self.error = error
        self.agent = agent
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "agent": self.agent,
            "timestamp": self.timestamp
        }

    def __str__(self):
        if self.success:
            return f"✅ {self.agent}: {self.data}"
        return f"❌ {self.agent}: {self.error}"
