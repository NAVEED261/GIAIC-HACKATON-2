"""
Base Agent Class for Phase-5 AI Employs
Provides MCP Tools interface and common functionality

@author: Phase-5 Multi-Agent System
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    handler: Callable = None

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


@dataclass
class AgentResult:
    """Result from agent execution"""
    success: bool
    data: Any = None
    error: str = None
    agent: str = None
    tool_used: str = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "agent": self.agent,
            "tool_used": self.tool_used,
            "timestamp": self.timestamp
        }


class BaseAgent(ABC):
    """
    Base class for all Phase-5 AI Employs

    Features:
    - MCP Tools registration
    - Self-reasoning capabilities
    - Smart execute_direct method
    - Status reporting
    """

    def __init__(self):
        self.name: str = "BaseAgent"
        self.domain: str = "base"
        self.description: str = "Base agent class"
        self.emoji: str = "🤖"
        self.tools: Dict[str, MCPTool] = {}
        self.is_working: bool = False
        self._setup_tools()

    @abstractmethod
    def _setup_tools(self):
        """Setup MCP tools - must be implemented by subclasses"""
        pass

    def register_tool(self, tool: MCPTool):
        """Register an MCP tool"""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a tool by name"""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict]:
        """List all available tools"""
        return [tool.to_dict() for tool in self.tools.values()]

    def get_status(self) -> Dict:
        """Get agent status"""
        return {
            "name": self.name,
            "domain": self.domain,
            "description": self.description,
            "emoji": self.emoji,
            "tools_count": len(self.tools),
            "is_working": self.is_working,
            "tools": list(self.tools.keys())
        }

    async def reason(self, query: str) -> List[Dict]:
        """
        Self-reasoning: Break down query into execution steps

        Returns list of steps to execute
        """
        steps = []
        query_lower = query.lower()

        # Default: single step with query
        steps.append({
            "step": 1,
            "action": "execute",
            "query": query,
            "tool": self._match_tool(query_lower)
        })

        return steps

    def _match_tool(self, query: str) -> Optional[str]:
        """Match query to best tool"""
        # Override in subclasses for domain-specific matching
        return None

    async def execute_tool(self, tool_name: str, **kwargs) -> AgentResult:
        """Execute a specific tool"""
        tool = self.get_tool(tool_name)

        if not tool:
            return AgentResult(
                success=False,
                error=f"Tool '{tool_name}' not found",
                agent=self.name
            )

        if not tool.handler:
            return AgentResult(
                success=False,
                error=f"Tool '{tool_name}' has no handler",
                agent=self.name
            )

        try:
            self.is_working = True
            result = await tool.handler(**kwargs)
            return AgentResult(
                success=True,
                data=result,
                agent=self.name,
                tool_used=tool_name
            )
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                agent=self.name,
                tool_used=tool_name
            )
        finally:
            self.is_working = False

    @abstractmethod
    async def execute_direct(self, step: Dict) -> Any:
        """
        Smart direct execution based on query
        Must be implemented by subclasses
        """
        pass

    async def process(self, query: str) -> AgentResult:
        """
        Main processing method
        1. Reason about query
        2. Execute steps
        3. Return result
        """
        try:
            self.is_working = True

            # Step 1: Reason
            steps = await self.reason(query)

            # Step 2: Execute
            results = []
            for step in steps:
                result = await self.execute_direct(step)
                results.append(result)

            # Step 3: Return
            return AgentResult(
                success=True,
                data=results[0] if len(results) == 1 else results,
                agent=self.name
            )

        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                agent=self.name
            )
        finally:
            self.is_working = False

    def __repr__(self):
        try:
            return f"{self.emoji} {self.name} ({len(self.tools)} tools)"
        except UnicodeEncodeError:
            return f"[{self.domain.upper()}] {self.name} ({len(self.tools)} tools)"
