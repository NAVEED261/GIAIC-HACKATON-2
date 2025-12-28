# Phase-5: Advanced Cloud Deployment Specification

## Overview

**Phase**: Phase-5 (Final Phase)
**Objective**: Implement advanced features and deploy to production-grade infrastructure
**Points**: 300 (Highest of all phases)
**Due Date**: Jan 18, 2026

---

## Phase-5 Parts

| Part | Description | Deployment | Card Required |
|------|-------------|------------|---------------|
| **Part A** | Advanced Features | Code Only | NO |
| **Part B** | Local Deployment | Minikube + Dapr | NO |
| **Part C** | Cloud Deployment | DOKS/GKE/AKS + Kafka | YES (Free credits) |

---

## Part A: Advanced Features

### Advanced Level Features (Required)

1. **Recurring Tasks**
   - Auto-reschedule repeating tasks
   - Patterns: daily, weekly, monthly, custom
   - Example: "weekly meeting" creates next occurrence on completion

2. **Due Dates & Time Reminders**
   - Set deadlines with date/time pickers
   - Browser notifications
   - Reminder scheduling (1 hour before, 1 day before, etc.)

### Intermediate Level Features (Required)

3. **Priorities**
   - Levels: high, medium, low
   - Visual indicators (colors)
   - Sort by priority

4. **Tags/Categories**
   - Labels: work, home, personal, urgent
   - Multiple tags per task
   - Filter by tags

5. **Search**
   - Search by keyword in title/description
   - Full-text search capability

6. **Filter**
   - Filter by status (pending, completed)
   - Filter by priority
   - Filter by date range
   - Filter by tags

7. **Sort**
   - Sort by due date
   - Sort by priority
   - Sort alphabetically
   - Sort by created date

---

## Part B: Local Deployment (Minikube + Dapr)

### Requirements

1. **Deploy to Minikube**
   - All Phase-3 services containerized
   - Kubernetes manifests ready
   - Helm charts configured

2. **Dapr Integration (Full)**
   - **Pub/Sub**: Kafka abstraction for events
   - **State Management**: Conversation state storage
   - **Service Invocation**: Frontend → Backend communication
   - **Bindings (Cron)**: Scheduled reminder triggers
   - **Secrets Management**: API keys, credentials

3. **Event-Driven Architecture**
   - Redpanda (Local Docker) for Kafka
   - Event topics: task-events, reminders, task-updates
   - Producers and Consumers

---

## Part C: Cloud Deployment (Future - Card Required)

### Requirements (For Later)

1. **Cloud Kubernetes** (Choose One)
   - DigitalOcean DOKS ($200 credit)
   - Google Cloud GKE ($300 credit)
   - Azure AKS ($200 credit)

2. **Kafka on Cloud**
   - Redpanda Cloud (FREE - No Card)

3. **CI/CD Pipeline**
   - GitHub Actions
   - Auto deploy on push

4. **Monitoring & Logging**
   - Health checks
   - Log aggregation

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Container Runtime | Docker Desktop | Local containers |
| Orchestration | Minikube | Local Kubernetes |
| Package Manager | Helm Charts | K8s deployments |
| Event Streaming | Redpanda (Local) | Kafka-compatible |
| Distributed Runtime | Dapr | Microservices abstraction |
| Backend | FastAPI + MCP | Phase-3 backend |
| Frontend | Next.js + ChatKit | Phase-3 frontend |
| Database | Neon PostgreSQL | Serverless DB |
| AI | OpenAI Agents SDK | Chatbot intelligence |

---

## AI Employs for Phase-5

| Agent | Domain | MCP Tools | Purpose |
|-------|--------|-----------|---------|
| KafkaAgent | Event Streaming | 12+ | Topics, Producers, Consumers |
| DaprAgent | Distributed Runtime | 15+ | Pub/Sub, State, Bindings |
| RecurringTaskAgent | Scheduling | 8+ | Cron patterns, recurrence |
| ReminderAgent | Notifications | 10+ | Due dates, alerts |
| FeatureAgent | Advanced Features | 12+ | Priority, Tags, Search, Filter, Sort |

---

## Database Schema Updates

### Task Model (Extended)

```python
class Task(SQLModel, table=True):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool = False

    # Phase-5 Advanced Features
    priority: str = "medium"  # high, medium, low
    tags: List[str] = []
    due_date: Optional[datetime]
    reminder_at: Optional[datetime]

    # Recurring Task Fields
    is_recurring: bool = False
    recurrence_pattern: Optional[str]  # daily, weekly, monthly, custom
    recurrence_interval: Optional[int]  # every N days/weeks/months
    parent_task_id: Optional[int]  # for recurring instances

    created_at: datetime
    updated_at: datetime
```

### New Models

```python
class Reminder(SQLModel, table=True):
    id: int
    task_id: int
    user_id: str
    remind_at: datetime
    sent: bool = False
    created_at: datetime

class Tag(SQLModel, table=True):
    id: int
    name: str
    user_id: str
    color: Optional[str]
```

---

## Kafka Topics

| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| task-events | Chat API (MCP) | Recurring Service, Audit | All CRUD operations |
| reminders | Chat API | Notification Service | Scheduled reminders |
| task-updates | Chat API | WebSocket Service | Real-time sync |

---

## Dapr Components

| Component | Type | Purpose |
|-----------|------|---------|
| kafka-pubsub | pubsub.kafka | Event streaming |
| statestore | state.postgresql | Conversation state |
| reminder-cron | bindings.cron | Scheduled triggers |
| kubernetes-secrets | secretstores.kubernetes | API keys |

---

## API Endpoints (New for Part A)

### Task Filtering & Sorting

```
GET /api/{user_id}/tasks?status=pending&priority=high&tags=work&sort=due_date
```

### Search

```
GET /api/{user_id}/tasks/search?q=meeting
```

### Recurring Tasks

```
POST /api/{user_id}/tasks
{
  "title": "Weekly Meeting",
  "is_recurring": true,
  "recurrence_pattern": "weekly",
  "recurrence_interval": 1
}
```

### Reminders

```
POST /api/{user_id}/tasks/{task_id}/reminder
{
  "remind_at": "2026-01-18T09:00:00Z"
}
```

---

## MCP Tools (New for Part A)

| Tool | Purpose |
|------|---------|
| set_priority | Set task priority (high/medium/low) |
| add_tags | Add tags to task |
| remove_tags | Remove tags from task |
| set_due_date | Set task due date |
| set_reminder | Schedule reminder |
| create_recurring | Create recurring task |
| search_tasks | Search tasks by keyword |
| filter_tasks | Filter by multiple criteria |
| sort_tasks | Sort tasks |

---

## Success Criteria

### Part A Complete When:
- [ ] All 7 features implemented (Recurring, Reminders, Priorities, Tags, Search, Filter, Sort)
- [ ] New MCP tools working
- [ ] Database schema updated
- [ ] API endpoints tested

### Part B Complete When:
- [ ] All services running on Minikube
- [ ] Dapr sidecar injected
- [ ] Kafka (Redpanda) events flowing
- [ ] Pub/Sub working
- [ ] State management working
- [ ] Cron bindings triggering
- [ ] Secrets properly managed

---

## Deliverables

1. **Code**: `Phase-5/` folder with all implementation
2. **Specs**: `Phase-5/specs/` with all specifications
3. **AI Employs**: `Phase-5/AI_EMPLOYS_PHZ_5/` with expert agents
4. **History**: `history/prompts/phase-5/` with all records
5. **README**: Setup and deployment instructions

---

*Specification Version: 1.0*
*Created: 2025-12-28*
*Author: Claude Code (Phase-5 Orchestrator)*
