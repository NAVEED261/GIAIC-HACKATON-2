"""
POWERFUL Multi-Agent System for Phase-4 Todo Application
15+ Specialized Agents with MCP Tools, Self-Reasoning, Multi-Step Execution

@author: Phase-4 Multi-Agent System

Agent Categories:
1. Infrastructure Agents: Docker, Kubernetes, Helm, Network
2. Application Agents: Task, Chat, Auth, Database
3. DevOps Agents: CICD, Monitoring, Security, Backup
4. Expert Agents: Architect, Debugger, Optimizer

Features:
- MCP Tools integration
- Self-reasoning with OpenAI GPT-4o-mini
- Multi-step execution plans
- Tool chaining
- Error recovery
- Visible agent execution
"""

from .base_agent import BaseAgent, MCPTool, AgentResult
from .orchestrator import Orchestrator

# Infrastructure
from .infrastructure import DockerAgent, KubernetesAgent, HelmAgent, NetworkAgent

# Application
from .application import TaskAgent, ChatAgent, AuthAgent, DatabaseAgent

# DevOps
from .devops import CICDAgent, MonitoringAgent, SecurityAgent, BackupAgent

# Expert
from .expert import ArchitectAgent, DebuggerAgent, OptimizerAgent

__all__ = [
    # Base
    'BaseAgent', 'MCPTool', 'AgentResult', 'Orchestrator',

    # Infrastructure
    'DockerAgent', 'KubernetesAgent', 'HelmAgent', 'NetworkAgent',

    # Application
    'TaskAgent', 'ChatAgent', 'AuthAgent', 'DatabaseAgent',

    # DevOps
    'CICDAgent', 'MonitoringAgent', 'SecurityAgent', 'BackupAgent',

    # Expert
    'ArchitectAgent', 'DebuggerAgent', 'OptimizerAgent'
]

__version__ = "1.0.0"
