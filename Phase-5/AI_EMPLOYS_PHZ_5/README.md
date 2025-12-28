# Phase-5 AI Employs System

Expert AI Agents for Todo Application - Advanced Features & Local Deployment

## Overview

The AI Employs System provides **8 specialized agents** with **96 MCP tools** for handling Phase-5 operations. Each agent is a domain expert that can be reused in other projects.

## Quick Start

```bash
cd Phase-5/AI_EMPLOYS_PHZ_5

# Interactive mode
python main.py

# Run all tests
python main.py --test

# Single query
python main.py --query "create kafka topic for tasks"

# List all agents
python main.py --agents
```

## Architecture

```
AI_EMPLOYS_PHZ_5/
├── main.py                 # Entry point
├── base_agent.py           # Base class for all agents
├── orchestrator.py         # Smart routing & delegation
│
├── infrastructure/         # Infrastructure Agents
│   ├── kafka_agent.py      # 12 tools - Event streaming
│   └── dapr_agent.py       # 15 tools - Distributed runtime
│
├── application/            # Application Agents
│   ├── feature_agent.py    # 12 tools - Priorities, tags, search
│   ├── recurring_agent.py  #  8 tools - Recurring tasks
│   └── reminder_agent.py   # 10 tools - Reminders & due dates
│
└── devops/                 # DevOps Agents
    ├── k8s_deploy_agent.py # 15 tools - Kubernetes deployment
    ├── helm_agent.py       # 12 tools - Helm chart management
    └── minikube_agent.py   # 12 tools - Local K8s cluster
```

## Available Agents

| Agent | Domain | Tools | Description |
|-------|--------|-------|-------------|
| KafkaAgent | kafka | 12 | Kafka/Redpanda event streaming |
| DaprAgent | dapr | 15 | Dapr distributed runtime |
| FeatureAgent | feature | 12 | Priorities, tags, search, filter, sort |
| RecurringAgent | recurring | 8 | Recurring task scheduling |
| ReminderAgent | reminder | 10 | Reminders and due dates |
| K8sDeployAgent | k8s | 15 | Kubernetes deployment |
| HelmAgent | helm | 12 | Helm chart management |
| MinikubeAgent | minikube | 12 | Local Kubernetes cluster |

**Total: 8 Agents, 96 MCP Tools**

## MCP Tools by Agent

### KafkaAgent (12 tools)
```
create_topic, delete_topic, list_topics, publish_event,
get_topic_info, check_kafka_health, get_consumer_groups,
get_topic_offsets, create_producer_config, create_consumer_config,
describe_cluster, test_connection
```

### DaprAgent (15 tools)
```
check_dapr_status, init_dapr, list_components, create_pubsub_component,
create_statestore, create_cron_binding, create_secretstore,
publish_message, save_state, get_state, invoke_service,
get_secret, list_dapr_apps, get_dapr_logs, generate_annotations
```

### FeatureAgent (12 tools)
```
set_priority, get_priorities, add_tags, remove_tags,
list_tags, create_tag, search_tasks, filter_tasks,
sort_tasks, get_filter_options, get_sort_options, advanced_query
```

### RecurringAgent (8 tools)
```
create_recurring_task, update_recurrence, stop_recurring,
get_recurrence_patterns, calculate_next_occurrence,
get_recurring_series, skip_occurrence, complete_recurring
```

### ReminderAgent (10 tools)
```
set_reminder, cancel_reminder, set_due_date, get_upcoming_reminders,
get_overdue_tasks, snooze_reminder, get_reminder_types,
update_reminder_preferences, schedule_notification, get_due_today
```

### K8sDeployAgent (15 tools)
```
apply_manifest, get_pods, get_deployments, get_services,
scale_deployment, get_pod_logs, describe_resource, create_namespace,
delete_resource, port_forward, get_events, rollout_status,
rollout_restart, get_configmaps, get_secrets
```

### HelmAgent (12 tools)
```
helm_install, helm_upgrade, helm_uninstall, helm_list,
helm_status, helm_template, helm_repo_add, helm_repo_update,
helm_search, helm_get_values, helm_rollback, helm_history
```

### MinikubeAgent (12 tools)
```
minikube_start, minikube_stop, minikube_delete, minikube_status,
enable_addon, list_addons, minikube_tunnel, docker_env,
minikube_ip, minikube_dashboard, minikube_service, minikube_ssh
```

## Smart Routing

The orchestrator uses keyword matching to route queries to the appropriate agent:

```python
# Examples of automatic routing:

"create kafka topic for tasks"      → KafkaAgent
"check dapr status"                 → DaprAgent
"set task priority to high"         → FeatureAgent
"create weekly recurring task"      → RecurringAgent
"set reminder for tomorrow"         → ReminderAgent
"deploy to kubernetes"              → K8sDeployAgent
"install helm chart"                → HelmAgent
"start minikube cluster"            → MinikubeAgent
```

## Usage Examples

### Programmatic Usage

```python
import asyncio
from orchestrator import AgentOrchestrator

async def main():
    # Initialize orchestrator (auto-registers all agents)
    orchestrator = AgentOrchestrator()

    # Delegate query to appropriate agent
    result = await orchestrator.delegate("create kafka topic for task-events")
    print(f"Agent: {result.agent}")
    print(f"Tool: {result.tool}")
    print(f"Result: {result.result}")

    # Direct agent access
    kafka_agent = orchestrator.get_agent("kafka")
    topics = await kafka_agent.process("list all topics")

asyncio.run(main())
```

### Direct Agent Usage

```python
from infrastructure.kafka_agent import KafkaAgent

async def use_kafka():
    agent = KafkaAgent()

    # Use specific tool
    result = await agent._create_topic(
        topic_name="task-events",
        partitions=3
    )
    print(result)

asyncio.run(use_kafka())
```

## Creating Custom Agents

Extend `BaseAgent` to create your own agent:

```python
from base_agent import BaseAgent, MCPTool, AgentResult

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "MyCustomAgent"
        self.domain = "custom"
        self.description = "My custom agent"
        self.emoji = "🎯"

    def _setup_tools(self):
        self.register_tool(MCPTool(
            name="my_tool",
            description="My custom tool",
            parameters={"input": "string"},
            handler=self._my_tool
        ))

    async def _my_tool(self, input: str):
        return {"result": f"Processed: {input}"}

    def _match_tool(self, query: str):
        return "my_tool"

    async def execute_direct(self, step):
        return await self._my_tool(step.get("input", ""))
```

## Reusability

These agents are designed to be **reusable across projects**:

1. **Copy the `AI_EMPLOYS_PHZ_5` folder** to your project
2. **Import and use agents** as needed
3. **Extend with custom agents** for your domain

## Requirements

- Python 3.8+
- No external dependencies for core functionality
- Optional: kubectl, helm, minikube, dapr CLI for actual operations

## License

Part of GIAIC Hackathon-2 Phase-5 Project
