# Part B: Local Deployment Specification (Minikube + Dapr)

## Overview

**Part**: B (Local Deployment)
**Type**: Infrastructure + Deployment
**Card Required**: NO (100% FREE)
**Dependencies**: Part A Complete, Docker Desktop, Minikube

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MINIKUBE CLUSTER                                   │
│                                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │
│  │   Frontend Pod      │  │   Backend Pod       │  │  Notification Pod   │  │
│  │ ┌───────┐ ┌───────┐ │  │ ┌───────┐ ┌───────┐ │  │ ┌───────┐ ┌───────┐ │  │
│  │ │ Next  │ │ Dapr  │ │  │ │FastAPI│ │ Dapr  │ │  │ │Notif  │ │ Dapr  │ │  │
│  │ │ App   │◀┼▶Sidecar│ │  │ │+ MCP  │◀┼▶Sidecar│ │  │ │Service│◀┼▶Sidecar│ │  │
│  │ └───────┘ └───────┘ │  │ └───────┘ └───────┘ │  │ └───────┘ └───────┘ │  │
│  └──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘  │
│             │                        │                        │              │
│             └────────────────────────┼────────────────────────┘              │
│                                      │                                       │
│                        ┌─────────────▼─────────────┐                        │
│                        │     DAPR COMPONENTS       │                        │
│                        │  ┌──────────────────────┐ │                        │
│                        │  │ pubsub.kafka         │─┼──▶ Redpanda (Local)    │
│                        │  ├──────────────────────┤ │                        │
│                        │  │ state.postgresql     │─┼──▶ Neon DB (External)  │
│                        │  ├──────────────────────┤ │                        │
│                        │  │ bindings.cron        │ │  (Scheduled triggers)  │
│                        │  ├──────────────────────┤ │                        │
│                        │  │ secretstores.k8s     │ │  (API keys)            │
│                        │  └──────────────────────┘ │                        │
│                        └───────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

| Tool | Version | Required | Installation |
|------|---------|----------|--------------|
| Docker Desktop | 4.25+ | YES | docker.com |
| Minikube | 1.32+ | YES | minikube.sigs.k8s.io |
| kubectl | 1.28+ | YES | kubernetes.io |
| Helm | 3.12+ | YES | helm.sh |
| Dapr CLI | 1.12+ | YES | dapr.io |

---

## Step 1: Minikube Setup

### Start Minikube

```bash
# Start with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify
kubectl get nodes
```

### Create Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-phase5
  labels:
    app: todo-chatbot
    phase: "5"
```

---

## Step 2: Dapr Installation

### Install Dapr on Kubernetes

```bash
# Install Dapr CLI (if not installed)
# Windows PowerShell:
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"

# Initialize Dapr on Kubernetes
dapr init -k --wait

# Verify Dapr installation
dapr status -k
kubectl get pods -n dapr-system
```

### Expected Dapr Pods

| Pod | Purpose |
|-----|---------|
| dapr-operator | Manages Dapr components |
| dapr-sentry | Certificate management |
| dapr-sidecar-injector | Injects sidecars into pods |
| dapr-placement | Actor placement service |
| dapr-dashboard | Web dashboard (optional) |

---

## Step 3: Redpanda (Local Kafka) Setup

### Deploy Redpanda on Minikube

```yaml
# k8s/redpanda.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redpanda
  namespace: todo-phase5
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redpanda
  template:
    metadata:
      labels:
        app: redpanda
    spec:
      containers:
      - name: redpanda
        image: redpandadata/redpanda:latest
        args:
          - redpanda
          - start
          - --smp=1
          - --memory=512M
          - --overprovisioned
          - --kafka-addr=PLAINTEXT://0.0.0.0:9092
          - --advertise-kafka-addr=PLAINTEXT://redpanda:9092
        ports:
        - containerPort: 9092
          name: kafka
        - containerPort: 8081
          name: schema-registry
        - containerPort: 8082
          name: rest-proxy
        resources:
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: redpanda
  namespace: todo-phase5
spec:
  selector:
    app: redpanda
  ports:
  - port: 9092
    targetPort: 9092
    name: kafka
  - port: 8081
    targetPort: 8081
    name: schema-registry
```

---

## Step 4: Dapr Components

### 4.1 Pub/Sub Component (Kafka)

```yaml
# dapr-components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: todo-phase5
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda.todo-phase5.svc.cluster.local:9092"
  - name: consumerGroup
    value: "todo-service"
  - name: authType
    value: "none"
```

### 4.2 State Store Component (PostgreSQL)

```yaml
# dapr-components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo-phase5
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: db-secrets
      key: connection-string
```

### 4.3 Cron Binding Component

```yaml
# dapr-components/cron-binding.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
  namespace: todo-phase5
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "*/5 * * * *"  # Every 5 minutes
```

### 4.4 Secret Store Component

```yaml
# dapr-components/secretstore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: todo-phase5
spec:
  type: secretstores.kubernetes
  version: v1
```

---

## Step 5: Kubernetes Secrets

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secrets
  namespace: todo-phase5
type: Opaque
stringData:
  connection-string: "postgresql://user:password@neon-host:5432/todo"
---
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
  namespace: todo-phase5
type: Opaque
stringData:
  openai-api-key: "sk-xxx"
  anthropic-api-key: "sk-ant-xxx"
  better-auth-secret: "your-secret-key"
```

---

## Step 6: Backend Deployment with Dapr

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-phase5
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: backend
        image: todo-backend:v5
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: connection-string
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-api-key
        - name: DAPR_HTTP_PORT
          value: "3500"
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: todo-backend-service
  namespace: todo-phase5
spec:
  selector:
    app: todo-backend
  ports:
  - port: 8000
    targetPort: 8000
```

---

## Step 7: Frontend Deployment with Dapr

```yaml
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: todo-phase5
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-frontend"
        dapr.io/app-port: "3000"
    spec:
      containers:
      - name: frontend
        image: todo-frontend:v5
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://localhost:3500/v1.0/invoke/todo-backend/method"
        - name: DAPR_HTTP_PORT
          value: "3500"
        resources:
          limits:
            memory: "256Mi"
            cpu: "250m"
---
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend-service
  namespace: todo-phase5
spec:
  type: NodePort
  selector:
    app: todo-frontend
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30080
```

---

## Step 8: Notification Service

```yaml
# k8s/notification-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notification-service
  namespace: todo-phase5
spec:
  replicas: 1
  selector:
    matchLabels:
      app: notification-service
  template:
    metadata:
      labels:
        app: notification-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "notification-service"
        dapr.io/app-port: "8001"
    spec:
      containers:
      - name: notification
        image: notification-service:v5
        ports:
        - containerPort: 8001
```

---

## Dapr Usage in Code

### Publish Event (Backend)

```python
# Instead of kafka-python
import httpx

async def publish_task_event(event_type: str, task_data: dict):
    """Publish event via Dapr sidecar"""
    dapr_url = "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events"

    await httpx.post(dapr_url, json={
        "event_type": event_type,
        "task_id": task_data["id"],
        "task_data": task_data,
        "timestamp": datetime.utcnow().isoformat()
    })
```

### Subscribe to Events (Notification Service)

```python
from fastapi import FastAPI

app = FastAPI()

# Dapr subscription
@app.get("/dapr/subscribe")
def subscribe():
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminders",
            "route": "/handle-reminder"
        }
    ]

@app.post("/handle-reminder")
async def handle_reminder(event: dict):
    """Handle reminder event from Kafka via Dapr"""
    task_id = event["data"]["task_id"]
    user_id = event["data"]["user_id"]
    # Send notification...
    return {"status": "ok"}
```

### State Management

```python
async def save_conversation_state(conv_id: str, messages: list):
    """Save state via Dapr"""
    dapr_url = f"http://localhost:3500/v1.0/state/statestore"

    await httpx.post(dapr_url, json=[{
        "key": f"conversation-{conv_id}",
        "value": {"messages": messages}
    }])

async def get_conversation_state(conv_id: str):
    """Get state via Dapr"""
    dapr_url = f"http://localhost:3500/v1.0/state/statestore/conversation-{conv_id}"

    response = await httpx.get(dapr_url)
    return response.json()
```

### Service Invocation (Frontend)

```typescript
// Instead of direct backend call
const response = await fetch(
  'http://localhost:3500/v1.0/invoke/todo-backend/method/api/chat',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userMessage })
  }
);
```

### Cron Handler

```python
@app.post("/reminder-cron")
async def check_reminders():
    """Called by Dapr cron binding every 5 minutes"""

    # Get tasks with due reminders
    due_reminders = await get_due_reminders()

    for reminder in due_reminders:
        # Publish reminder event
        await publish_reminder_event(reminder)
        # Mark as sent
        await mark_reminder_sent(reminder.id)

    return {"processed": len(due_reminders)}
```

---

## Deployment Commands

```bash
# 1. Build Docker images
docker build -t todo-backend:v5 -f Phase-5/docker/backend/Dockerfile .
docker build -t todo-frontend:v5 -f Phase-5/docker/frontend/Dockerfile .
docker build -t notification-service:v5 -f Phase-5/docker/notification/Dockerfile .

# 2. Load images to Minikube
minikube image load todo-backend:v5
minikube image load todo-frontend:v5
minikube image load notification-service:v5

# 3. Apply configurations
kubectl apply -f Phase-5/k8s/namespace.yaml
kubectl apply -f Phase-5/k8s/secrets.yaml
kubectl apply -f Phase-5/k8s/redpanda.yaml
kubectl apply -f Phase-5/dapr-components/
kubectl apply -f Phase-5/k8s/backend-deployment.yaml
kubectl apply -f Phase-5/k8s/frontend-deployment.yaml
kubectl apply -f Phase-5/k8s/notification-deployment.yaml

# 4. Verify deployments
kubectl get pods -n todo-phase5
dapr list -k

# 5. Access application
minikube service todo-frontend-service -n todo-phase5 --url
```

---

## Verification Checklist

### Minikube
- [ ] Minikube running
- [ ] All pods in Running state
- [ ] Services accessible

### Dapr
- [ ] Dapr sidecars injected (2 containers per pod)
- [ ] Dapr components created
- [ ] `dapr list -k` shows all apps

### Kafka (Redpanda)
- [ ] Redpanda pod running
- [ ] Topics created (task-events, reminders, task-updates)
- [ ] Events flowing

### Dapr Features
- [ ] Pub/Sub working (publish/subscribe)
- [ ] State management working (save/get state)
- [ ] Cron binding triggering
- [ ] Secrets accessible

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pod CrashLoopBackOff | Check logs: `kubectl logs <pod> -n todo-phase5` |
| Dapr sidecar not injected | Verify annotation: `dapr.io/enabled: "true"` |
| Kafka connection refused | Check Redpanda service: `kubectl get svc -n todo-phase5` |
| State store error | Verify PostgreSQL connection string |

---

*Part B Specification Version: 1.0*
*Created: 2025-12-28*
