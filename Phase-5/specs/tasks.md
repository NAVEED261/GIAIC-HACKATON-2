# Phase-5 Tasks

## Part A: Advanced Features

### A1. Database Schema Updates
- [ ] Add `priority` column to tasks table (enum: low/medium/high/urgent)
- [ ] Add `due_date` column to tasks table (timestamp)
- [ ] Add `is_recurring` column to tasks table (boolean)
- [ ] Add `recurrence_pattern` column (daily/weekly/monthly)
- [ ] Add `recurrence_interval` column (int)
- [ ] Create `tags` table (id, name, color, user_id)
- [ ] Create `task_tags` junction table (task_id, tag_id)
- [ ] Create `reminders` table (id, task_id, remind_at, type, status)

### A2. Recurring Tasks Implementation
- [ ] Create RecurringTaskService
- [ ] Implement create_recurring_task endpoint
- [ ] Implement next occurrence calculation
- [ ] Implement skip/complete recurring task
- [ ] Add Kafka event: recurring_task_created
- [ ] Add Kafka event: recurring_task_completed

### A3. Reminders & Due Dates
- [ ] Create ReminderService
- [ ] Implement set_reminder endpoint
- [ ] Implement due_date update endpoint
- [ ] Implement get_overdue_tasks endpoint
- [ ] Create notification service (Dapr binding)
- [ ] Add Kafka topic: reminders

### A4. Priority System
- [ ] Add priority to task model
- [ ] Update create/update task endpoints
- [ ] Add priority-based sorting
- [ ] Add priority filter

### A5. Tags & Categories
- [ ] Create Tag model and endpoints
- [ ] Implement add_tags_to_task
- [ ] Implement remove_tags_from_task
- [ ] Implement filter_by_tags

### A6. Search, Filter, Sort
- [ ] Implement full-text search
- [ ] Add filter by: status, priority, due_date, tags
- [ ] Add sort by: created_at, due_date, priority, title
- [ ] Combine filters and sorting

---

## Part B: Local Deployment (Minikube + Dapr)

### B1. Minikube Setup
- [ ] Create Minikube start script
- [ ] Enable required addons (ingress, metrics-server)
- [ ] Create namespace: todo-phase5

### B2. Dapr Installation
- [ ] Install Dapr CLI
- [ ] Initialize Dapr on Minikube
- [ ] Verify Dapr components

### B3. Dapr Components
- [ ] Create kafka-pubsub.yaml (Redpanda)
- [ ] Create statestore.yaml (Redis)
- [ ] Create cron-binding.yaml (reminders)
- [ ] Create secretstore.yaml (Kubernetes secrets)
- [ ] Apply all components to cluster

### B4. Redpanda/Kafka Setup
- [ ] Create Redpanda Helm values
- [ ] Deploy Redpanda to Minikube
- [ ] Create topics: task-events, reminders, task-updates
- [ ] Verify pub/sub with Dapr

### B5. Application Deployment
- [ ] Create backend Dockerfile
- [ ] Create frontend Dockerfile
- [ ] Create backend Helm chart
- [ ] Create frontend Helm chart
- [ ] Add Dapr annotations to deployments
- [ ] Deploy PostgreSQL
- [ ] Deploy Redis
- [ ] Deploy backend with Dapr sidecar
- [ ] Deploy frontend

### B6. Notification Service
- [ ] Create notification-service
- [ ] Subscribe to reminders topic
- [ ] Process reminder notifications
- [ ] Deploy with Dapr sidecar

### B7. Testing & Verification
- [ ] Test all Dapr pub/sub
- [ ] Test state management
- [ ] Test service invocation
- [ ] Test cron binding for reminders
- [ ] End-to-end test: create recurring task → reminder → notification

---

## Dependencies

```
A1 (Schema) → A2, A3, A4, A5, A6
B1 (Minikube) → B2, B4, B5
B2 (Dapr) → B3
B3 (Components) → B5, B6
B4 (Redpanda) → B3, B5
```

---

## Estimated Effort

| Task Group | Items | Priority |
|------------|-------|----------|
| A1: Schema | 8 | HIGH |
| A2: Recurring | 6 | HIGH |
| A3: Reminders | 6 | HIGH |
| A4: Priority | 4 | MEDIUM |
| A5: Tags | 4 | MEDIUM |
| A6: Search | 4 | MEDIUM |
| B1: Minikube | 3 | HIGH |
| B2: Dapr | 3 | HIGH |
| B3: Components | 5 | HIGH |
| B4: Redpanda | 4 | HIGH |
| B5: App Deploy | 9 | HIGH |
| B6: Notification | 4 | MEDIUM |
| B7: Testing | 5 | HIGH |

**Total: 65 tasks**
