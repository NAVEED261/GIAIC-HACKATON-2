"""
Phase-5 AI Employs System
Expert Agents for Advanced Features & Local Deployment

@author: Phase-5 Multi-Agent System

AI Employs Available:
---------------------
1. KafkaAgent      (12 tools) - Event streaming
2. DaprAgent       (15 tools) - Distributed runtime
3. FeatureAgent    (12 tools) - Task features
4. RecurringAgent   (8 tools) - Recurring tasks
5. ReminderAgent   (10 tools) - Reminders & due dates
6. K8sDeployAgent  (15 tools) - Kubernetes deployment
7. HelmAgent       (12 tools) - Helm chart management
8. MinikubeAgent   (12 tools) - Local K8s cluster

Total: 8 Agents, 96 MCP Tools
"""

from .base_agent import BaseAgent, MCPTool, AgentResult
from .orchestrator import AgentOrchestrator

# Infrastructure Agents
from .infrastructure import KafkaAgent, DaprAgent

# Application Agents
from .application import FeatureAgent, RecurringAgent, ReminderAgent

# DevOps Agents
from .devops import K8sDeployAgent, HelmAgent, MinikubeAgent

__all__ = [
    # Core
    'BaseAgent',
    'MCPTool',
    'AgentResult',
    'AgentOrchestrator',

    # Infrastructure
    'KafkaAgent',
    'DaprAgent',

    # Application
    'FeatureAgent',
    'RecurringAgent',
    'ReminderAgent',

    # DevOps
    'K8sDeployAgent',
    'HelmAgent',
    'MinikubeAgent',
]

__version__ = '1.0.0'
__phase__ = '5'
__total_agents__ = 8
__total_tools__ = 96
