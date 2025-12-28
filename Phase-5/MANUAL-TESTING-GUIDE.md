# Phase-5 Manual Testing Guide

## Quick Start - Roman Urdu Instructions

### Step 1: AI Employs Test Karo

```bash
cd Phase-5/AI_EMPLOYS_PHZ_5
python -c "from orchestrator import AgentOrchestrator; o = AgentOrchestrator(); print(o.get_status())"
```

**Expected Output**: 8 agents registered, 96 tools

---

### Step 2: Backend Test Karo

```bash
cd Phase-5/backend
python -c "from main import app; print(f'Routes: {len(app.routes)}')"
```

**Expected Output**: Routes: 45

---

### Step 3: Notification Service Test Karo

```bash
cd Phase-5/notification-service
python -c "from main import app; print(f'Routes: {len(app.routes)}')"
```

**Expected Output**: Routes: 8

---

## Complete Testing Commands

### Test 1: AI Employs Agents (8 Agents)

```bash
cd "D:\PIAIC HACKATON PRACTICE\GIAIC-HACKATON-2\Phase-5\AI_EMPLOYS_PHZ_5"

python -c "
from infrastructure.kafka_agent import KafkaAgent
from infrastructure.dapr_agent import DaprAgent
from application.feature_agent import FeatureAgent
from application.recurring_agent import RecurringAgent
from application.reminder_agent import ReminderAgent
from devops.k8s_deploy_agent import K8sDeployAgent
from devops.helm_agent import HelmAgent
from devops.minikube_agent import MinikubeAgent

agents = [KafkaAgent(), DaprAgent(), FeatureAgent(), RecurringAgent(),
          ReminderAgent(), K8sDeployAgent(), HelmAgent(), MinikubeAgent()]
print(f'Total Agents: {len(agents)}')
for a in agents:
    print(f'  {a.name}: {len(a.tools)} tools')
"
```

### Test 2: MCP Tools (96 Tools)

```bash
python -c "
from orchestrator import AgentOrchestrator
o = AgentOrchestrator()
total = sum(len(a.tools) for a in o.agents.values())
print(f'Total MCP Tools: {total}')
"
```

### Test 3: Smart Routing

```bash
python -c "
import asyncio
from orchestrator import AgentOrchestrator

async def test():
    o = AgentOrchestrator()
    result = await o.delegate('Create a Kafka topic')
    print(f'Result: {result.success}, Agent: {result.agent}')

asyncio.run(test())
"
```

### Test 4: Backend Models

```bash
cd "D:\PIAIC HACKATON PRACTICE\GIAIC-HACKATON-2\Phase-5\backend"

python -c "
from models.task import Task, Priority, RecurrencePattern
from models.user import User
from models.tag import Tag
from models.reminder import Reminder, ReminderType
print('All models OK')
"
```

### Test 5: Backend Services

```bash
python -c "
from services.task_service import TaskService
from services.tag_service import TagService
from services.reminder_service import ReminderService
from services.recurring_service import RecurringTaskService
print('All services OK')
"
```

### Test 6: Backend Routes

```bash
python -c "
from routes.tasks import router as tasks
from routes.tags import router as tags
from routes.reminders import router as reminders
print('All routes OK')
"
```

### Test 7: Main App

```bash
python -c "
from main import app
print(f'App: {app.title}')
print(f'Routes: {len(app.routes)}')
"
```

---

## Local Development Testing

### Option A: Run Backend Only (No Database)

```bash
cd Phase-5/backend

# Set environment
set DATABASE_URL=postgresql://user:pass@localhost:5432/db
set JWT_SECRET=test-secret-key-32-chars-minimum

# Start server (will fail on DB connect, but app loads)
python -c "from main import app; print('App loads OK')"
```

### Option B: Run with Docker Compose

```bash
cd Phase-5

# Create docker-compose.yml
docker-compose up -d postgres redis
docker-compose up backend frontend
```

### Option C: Run with Minikube + Dapr

```bash
# Start Minikube
minikube start --driver=docker --cpus=4 --memory=8192

# Install Dapr
dapr init -k

# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f backend/dapr_components/

# Build and deploy
docker build -t todo-backend:v1 -f backend/Dockerfile backend/
docker build -t todo-frontend:v1 -f frontend/Dockerfile frontend/

kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

---

## Verification Checklist

- [ ] 8 AI Employs agents load
- [ ] 96 MCP tools registered
- [ ] Smart routing works (8/8)
- [ ] Backend models import
- [ ] Backend services import
- [ ] Backend routes import
- [ ] main.py loads (45 routes)
- [ ] notification-service loads
- [ ] K8s YAML valid (7 files)
- [ ] Dapr components valid (4 files)

---

## Expected Test Results

### AI Employs
```
Total Agents: 8
  KafkaAgent: 12 tools
  DaprAgent: 15 tools
  FeatureAgent: 12 tools
  RecurringAgent: 8 tools
  ReminderAgent: 10 tools
  K8sDeployAgent: 15 tools
  HelmAgent: 12 tools
  MinikubeAgent: 12 tools
Total: 96 MCP Tools
```

### Backend
```
Models: OK
Services: OK
Routes: OK
App: Phase-5 Todo API
Routes: 45
```

### Notification Service
```
App: Notification Service
Routes: 8
```

---

## Troubleshooting

### Error: Module not found
```bash
cd Phase-5/backend
set PYTHONPATH=%cd%
python -c "from main import app"
```

### Error: Database connection
This is expected without PostgreSQL running. The app structure is correct.

### Error: Emoji encoding (Windows)
Fixed in orchestrator.py - will show `[*]` instead of emoji.

---

## Contact

If any test fails, check:
1. Python 3.11+ installed
2. Current directory is correct
3. All files are present

Phase-5 Part A & B: 100% COMPLETE
