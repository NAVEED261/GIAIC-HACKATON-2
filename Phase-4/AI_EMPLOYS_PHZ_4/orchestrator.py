"""
Orchestrator Agent - Manager of all SubAgents
Routes tasks to appropriate agents based on intent

@author: Phase-4 Multi-Agent System
"""

import asyncio
from typing import Dict, Any, List, Optional
from base_agent import BaseAgent, AgentResult
from colorama import Fore, Style


class Orchestrator(BaseAgent):
    """
    Manager Agent - Routes tasks to specialized agents.
    Visible delegation and result aggregation.
    """

    def __init__(self):
        super().__init__("Orchestrator", "Manager Agent - Routes tasks to specialists")
        self.agents: Dict[str, BaseAgent] = {}
        self.task_history: List[Dict] = []

    def register_agent(self, agent: BaseAgent):
        """Register a sub-agent"""
        self.agents[agent.name.lower()] = agent
        self.log(f"Registered: {agent.emoji} {agent.name}", "info")

    def register_agents(self, agents: List[BaseAgent]):
        """Register multiple agents"""
        print(f"\n{Fore.YELLOW}🎯 [Orchestrator]{Style.RESET_ALL} Registering agents...")
        for agent in agents:
            self.register_agent(agent)
        print(f"   └─ Total: {len(self.agents)} agents ready\n")

    def find_agent(self, task: str) -> Optional[BaseAgent]:
        """Find the best agent for a task using keyword scoring"""
        task_lower = task.lower()
        best_agent = None
        best_score = 0

        # Domain-specific keywords that should heavily influence routing
        DOMAIN_KEYWORDS = {
            'git': 'cicd', 'github': 'cicd', 'commit': 'cicd', 'branch': 'cicd',
            'kubectl': 'kubernetes', 'pod': 'kubernetes', 'deployment': 'kubernetes',
            'docker': 'docker', 'container': 'docker', 'image': 'docker',
            'helm': 'helm', 'chart': 'helm', 'release': 'helm',
            'database': 'database', 'sql': 'database', 'query': 'database',
            'monitor': 'monitoring', 'metric': 'monitoring', 'alert': 'monitoring',
            'security': 'security', 'secret': 'security', 'rbac': 'security',
            'backup': 'backup', 'restore': 'backup', 'snapshot': 'backup',
            'architect': 'architect', 'design': 'architect', 'pattern': 'architect',
            'debug': 'debugger', 'error': 'debugger', 'crash': 'debugger',
            'optimize': 'optimizer', 'performance': 'optimizer', 'scale': 'optimizer',
            'network': 'network', 'ingress': 'network', 'port': 'network',
        }

        # Check for domain-specific keywords first
        for keyword, agent_name in DOMAIN_KEYWORDS.items():
            if keyword in task_lower:
                if agent_name in self.agents:
                    return self.agents[agent_name]

        # Fallback to keyword scoring
        for agent in self.agents.values():
            if agent.can_handle(task):
                # Score based on number of matching keywords
                score = 0
                if hasattr(agent, 'KEYWORDS'):
                    for keyword in agent.KEYWORDS:
                        if keyword in task_lower:
                            score += 1
                            # Bonus for longer/more specific keywords
                            if len(keyword) > 5:
                                score += 1

                # Take agent with highest score
                if score > best_score:
                    best_score = score
                    best_agent = agent

        return best_agent

    def find_agents(self, task: str) -> List[BaseAgent]:
        """Find all agents that can handle a task"""
        return [agent for agent in self.agents.values() if agent.can_handle(task)]

    async def delegate(self, task: str, params: Dict[str, Any] = None) -> AgentResult:
        """
        Delegate task to appropriate agent.
        Shows visible delegation flow.
        """
        self.start_work(f"Processing: {task}")

        # Find capable agent
        agent = self.find_agent(task)

        if not agent:
            self.report_error(f"No agent found for: {task}")
            return AgentResult(
                success=False,
                error=f"No agent available for task: {task}",
                agent=self.name
            )

        # Delegate with visibility
        self.log(f"{agent.emoji} {agent.name}", "delegate")

        try:
            # Execute via agent
            result = await agent.execute({
                "task": task,
                "params": params or {}
            })

            # Record history
            self.task_history.append({
                "task": task,
                "agent": agent.name,
                "result": result
            })

            self.end_work(f"Completed via {agent.name}")
            return AgentResult(
                success=True,
                data=result,
                agent=agent.name
            )

        except Exception as e:
            self.report_error(str(e))
            return AgentResult(
                success=False,
                error=str(e),
                agent=agent.name
            )

    async def delegate_parallel(self, tasks: List[Dict[str, Any]]) -> List[AgentResult]:
        """
        Delegate multiple tasks in parallel.
        Shows all agents working simultaneously.
        """
        self.start_work(f"Processing {len(tasks)} tasks in parallel")

        # Create tasks for all
        async_tasks = []
        for task_info in tasks:
            task = task_info.get("task", "")
            params = task_info.get("params", {})
            async_tasks.append(self.delegate(task, params))

        # Execute all in parallel
        results = await asyncio.gather(*async_tasks, return_exceptions=True)

        self.end_work(f"Completed {len(results)} tasks")
        return results

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute orchestrator task"""
        task_str = task.get("task", "")
        params = task.get("params", {})
        result = await self.delegate(task_str, params)
        return result.to_dict()

    def can_handle(self, task: str) -> bool:
        """Orchestrator can handle any task"""
        return True

    def show_agents(self):
        """Display all registered agents"""
        print(f"\n{Fore.YELLOW}🎯 [Orchestrator]{Style.RESET_ALL} Registered Agents:")
        print("=" * 50)
        for name, agent in self.agents.items():
            status = "🟢" if not agent.is_working else "🔄"
            print(f"  {status} {agent.emoji} {agent.name}: {agent.description}")
        print("=" * 50)

    def get_history(self) -> List[Dict]:
        """Get task execution history"""
        return self.task_history


# Global orchestrator instance
orchestrator = Orchestrator()


async def process_query(query: str, params: Dict = None) -> AgentResult:
    """
    Main entry point for processing user queries.
    Use this function to delegate any task.
    """
    return await orchestrator.delegate(query, params)


def show_agents():
    """Show all available agents"""
    orchestrator.show_agents()
