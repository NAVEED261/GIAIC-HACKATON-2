# Phase-5: Advanced Features & Local Deployment

**Status**: IN PROGRESS

## Overview

Phase-5 implements advanced todo features with local Kubernetes deployment using Minikube and Dapr.

### Part A: Advanced Features (Complete)
- Recurring Tasks (daily/weekly/monthly)
- Due Dates & Reminders
- Task Priorities (low/medium/high/urgent)
- Tags & Categories
- Search, Filter, Sort

### Part B: Local Deployment (Complete)
- Minikube (Local Kubernetes)
- Dapr (Distributed Runtime)
- Kafka/Redpanda (Event Streaming)

### Part C: Cloud Deployment (Pending)
- DigitalOcean / GKE / AKS
- CI/CD Pipeline

## Quick Start

### Prerequisites
- Docker Desktop
- Minikube
- kubectl
- Helm
- Dapr CLI

### Deploy Locally
```bash
cd Phase-5
chmod +x scripts/deploy-local.sh
./scripts/deploy-local.sh
```

### Access Application
```bash
# Start tunnel (in separate terminal)
minikube tunnel

# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

## Project Structure

```
Phase-5/
├── specs/                    # Specifications
│   ├── spec.md              # Main spec
│   ├── plan.md              # Implementation plan
│   ├── tasks.md             # Task checklist
│   └── features/            # Feature specs
│
├── AI_EMPLOYS_PHZ_5/        # AI Agents (8 agents, 96 tools)
│   ├── infrastructure/      # Kafka, Dapr agents
│   ├── application/         # Feature, Recurring, Reminder agents
│   └── devops/              # K8s, Helm, Minikube agents
│
├── backend/                  # FastAPI Backend
│   ├── models/              # SQLModel entities
│   ├── services/            # Business logic
│   ├── routes/              # API endpoints
│   └── dapr_components/     # Dapr YAML configs
│
├── k8s/                      # Kubernetes manifests
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── ...
│
└── scripts/                  # Deployment scripts
    └── deploy-local.sh
```

## API Endpoints

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /tasks | Create task |
| GET | /tasks | List tasks (with filters) |
| GET | /tasks/{id} | Get task |
| PATCH | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |
| POST | /tasks/{id}/complete | Complete task |
| POST | /tasks/{id}/priority | Set priority |
| POST | /tasks/{id}/due-date | Set due date |
| POST | /tasks/{id}/tags | Add tags |
| POST | /tasks/{id}/skip | Skip recurring |
| POST | /tasks/{id}/stop-recurring | Stop recurring |

### Tags
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /tags | Create tag |
| GET | /tags | List tags |
| PATCH | /tags/{id} | Update tag |
| DELETE | /tags/{id} | Delete tag |

### Reminders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /reminders | Create reminder |
| GET | /reminders | List upcoming |
| GET | /reminders/overdue | Get overdue tasks |
| POST | /reminders/{id}/snooze | Snooze reminder |
| DELETE | /reminders/{id} | Cancel reminder |

## Dapr Components

| Component | Type | Purpose |
|-----------|------|---------|
| kafka-pubsub | pubsub.kafka | Event messaging |
| statestore | state.redis | State management |
| reminder-cron | bindings.cron | Reminder scheduling |
| kubernetes-secrets | secretstores.kubernetes | Secret management |

## Kafka Topics

| Topic | Purpose |
|-------|---------|
| task-events | Task CRUD events |
| reminders | Reminder scheduling |
| notifications | Notification delivery |

## AI Employs System

8 Expert Agents with 96 MCP Tools:

| Agent | Tools | Domain |
|-------|-------|--------|
| KafkaAgent | 12 | Event streaming |
| DaprAgent | 15 | Distributed runtime |
| FeatureAgent | 12 | Task features |
| RecurringAgent | 8 | Recurring tasks |
| ReminderAgent | 10 | Reminders |
| K8sDeployAgent | 15 | Kubernetes |
| HelmAgent | 12 | Helm charts |
| MinikubeAgent | 12 | Local K8s |

### Usage
```bash
cd AI_EMPLOYS_PHZ_5
python main.py --agents       # List all agents
python main.py --test         # Run tests
python main.py                # Interactive mode
```

## Commands

```bash
# Check pods
kubectl get pods -n todo-phase5

# Check Dapr status
dapr status -k

# View logs
kubectl logs -l app=backend -n todo-phase5

# List Kafka topics
kubectl exec -it redpanda-0 -n todo-phase5 -- rpk topic list
```

## Part A Features

### Priority System
```python
# Priority levels
LOW = "low"
MEDIUM = "medium"  # default
HIGH = "high"
URGENT = "urgent"
```

### Recurring Tasks
```python
# Patterns
DAILY = "daily"      # Every N days
WEEKLY = "weekly"    # Every N weeks
MONTHLY = "monthly"  # Every N months
CUSTOM = "custom"    # Custom interval
```

### Reminders
```python
# Reminder types
EMAIL = "email"
PUSH = "push"        # default
SMS = "sms"
IN_APP = "in_app"
```

## License

Part of GIAIC Hackathon-2 Project
