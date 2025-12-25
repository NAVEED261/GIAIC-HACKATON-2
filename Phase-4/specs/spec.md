# Phase-4: Kubernetes Deployment Specification

## Overview

**Phase**: 4 - Container Orchestration & Kubernetes Deployment
**Objective**: Deploy Phase-3 Todo Chatbot on local Kubernetes cluster using Minikube
**Status**: In Development

---

## Context from Hackathon-2

### Phase-4 Objective (As per Hackathon-2 PDF)
Deploy Todo Chatbot (Phase-3) on a local Kubernetes cluster using:
- Docker containerization
- Minikube for local Kubernetes
- Helm Charts for package management
- AI-assisted DevOps tools

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Containerization | Docker | Package applications into containers |
| Docker AI | Gordon (Docker AI Agent) | AI-assisted Docker operations |
| Orchestration | Kubernetes (Minikube) | Container orchestration locally |
| Package Manager | Helm Charts | Kubernetes package management |
| AI DevOps | kubectl-ai | AI-assisted kubectl commands |
| AI Agent | Kagent | Kubernetes AI Agent for operations |

---

## Environment Requirements

### Verified Environment (User's System)
```
- OS: Windows 11
- Docker Desktop: v28.3.2 (RUNNING)
- Minikube: v1.37.0 (RUNNING with Docker driver)
- Kubernetes: Running on Minikube
  - host: Running
  - kubelet: Running
  - apiserver: Running
  - kubeconfig: Configured
```

### Additional Requirements
- kubectl CLI (included with Minikube)
- Helm 3.x
- kubectl-ai (optional, for AI-assisted operations)
- Docker AI / Gordon (optional, for AI-assisted Docker)

---

## Architecture

### Deployment Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      MINIKUBE CLUSTER                        │
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │   Ingress       │     │        Namespace: todo      │   │
│  │   Controller    │────▶│  ┌─────────┐  ┌──────────┐  │   │
│  └─────────────────┘     │  │Frontend │  │ Backend  │  │   │
│                          │  │ Service │  │ Service  │  │   │
│                          │  └────┬────┘  └────┬─────┘  │   │
│                          │       │            │        │   │
│                          │  ┌────▼────┐  ┌────▼─────┐  │   │
│                          │  │Frontend │  │ Backend  │  │   │
│                          │  │   Pod   │  │   Pod    │  │   │
│                          │  │(Next.js)│  │(FastAPI) │  │   │
│                          │  └─────────┘  └──────────┘  │   │
│                          └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   External Access    │
                    │  minikube tunnel /   │
                    │  NodePort / Ingress  │
                    └─────────────────────┘
```

### Container Architecture
```
┌────────────────────────────────────────┐
│           Frontend Container            │
│  ┌────────────────────────────────┐    │
│  │  Next.js Application           │    │
│  │  - Static Assets (SSG)         │    │
│  │  - API Routes (if any)         │    │
│  │  - ChatKit Component           │    │
│  │  Port: 3000                    │    │
│  └────────────────────────────────┘    │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│           Backend Container             │
│  ┌────────────────────────────────┐    │
│  │  FastAPI Application           │    │
│  │  - REST API Endpoints          │    │
│  │  - MCP Tools Integration       │    │
│  │  - Claude AI Integration       │    │
│  │  Port: 8000                    │    │
│  └────────────────────────────────┘    │
└────────────────────────────────────────┘
```

---

## Domain-Specific SubAgents

### 1. Docker Agent
**Purpose**: Containerization and Docker operations
**Location**: `Phase-4/agents/docker-agent/`
**Expertise**:
- Dockerfile creation and optimization
- Multi-stage builds
- Image management
- Docker Compose
- Docker AI (Gordon) integration

### 2. Kubernetes Agent
**Purpose**: Kubernetes deployment and management
**Location**: `Phase-4/agents/kubernetes-agent/`
**Expertise**:
- Kubernetes manifests (Deployment, Service, ConfigMap)
- Minikube operations
- kubectl commands
- kubectl-ai integration
- Namespace management

### 3. Helm Agent
**Purpose**: Helm chart creation and management
**Location**: `Phase-4/agents/helm-agent/`
**Expertise**:
- Helm chart structure
- values.yaml configuration
- Template functions
- Chart dependencies
- Release management

### 4. AIOps Agent
**Purpose**: AI-assisted DevOps operations
**Location**: `Phase-4/agents/aiops-agent/`
**Expertise**:
- Docker AI (Gordon) commands
- kubectl-ai integration
- Kagent operations
- Automated troubleshooting
- AI-driven deployments

---

## Containerization Specifications

### Frontend Dockerfile Requirements
```dockerfile
# Base: Node.js 18+ Alpine
# Build stage: Install dependencies, build Next.js
# Production stage: Minimal runtime
# Exposed port: 3000
# Health check: HTTP endpoint
```

### Backend Dockerfile Requirements
```dockerfile
# Base: Python 3.11+ Slim
# Install dependencies from requirements.txt
# Copy application code
# Exposed port: 8000
# Health check: /health endpoint
# Environment variables for configuration
```

### Docker Compose (Local Testing)
- Frontend service
- Backend service
- Network: todo-network
- Volume mounts for development

---

## Kubernetes Specifications

### Namespace
- Name: `todo`
- Purpose: Isolate Todo application resources

### Frontend Deployment
- Replicas: 2
- Image: todo-frontend:latest
- Resource limits: CPU 500m, Memory 512Mi
- Liveness/Readiness probes
- ConfigMap for environment variables

### Backend Deployment
- Replicas: 2
- Image: todo-backend:latest
- Resource limits: CPU 500m, Memory 512Mi
- Liveness/Readiness probes
- Secrets for API keys
- ConfigMap for configuration

### Services
- Frontend: ClusterIP (internal), NodePort (external access)
- Backend: ClusterIP (internal), NodePort (external access)

### Ingress (Optional)
- Host-based routing
- Path-based routing to frontend/backend

---

## Helm Chart Specifications

### Chart Structure
```
helm-charts/
├── todo-frontend/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── _helpers.tpl
│   └── .helmignore
│
└── todo-backend/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── configmap.yaml
    │   ├── secret.yaml
    │   └── _helpers.tpl
    └── .helmignore
```

### Values Configuration
- Image repository and tag
- Replica count
- Resource limits
- Environment variables
- Service type and ports

---

## AIOps Integration

### Docker AI (Gordon)
```bash
# AI-assisted Dockerfile generation
docker ai "create optimized Dockerfile for Next.js app"

# AI-assisted troubleshooting
docker ai "why is my container not starting"
```

### kubectl-ai
```bash
# AI-assisted deployment
kubectl-ai "deploy the todo app with 2 replicas"

# AI-assisted debugging
kubectl-ai "why are pods crashing in todo namespace"
```

### Kagent
- Autonomous Kubernetes agent
- AI-driven operations
- Automated scaling decisions
- Intelligent troubleshooting

---

## Deployment Workflow

### Step 1: Build Docker Images
```bash
# Build frontend
docker build -t todo-frontend:latest ./Phase-4/docker/frontend

# Build backend
docker build -t todo-backend:latest ./Phase-4/docker/backend
```

### Step 2: Load Images to Minikube
```bash
# Load images into Minikube's Docker
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### Step 3: Deploy with Helm
```bash
# Create namespace
kubectl create namespace todo

# Deploy backend
helm install todo-backend ./Phase-4/helm-charts/todo-backend -n todo

# Deploy frontend
helm install todo-frontend ./Phase-4/helm-charts/todo-frontend -n todo
```

### Step 4: Access Application
```bash
# Get service URLs
minikube service todo-frontend -n todo --url
minikube service todo-backend -n todo --url

# Or use tunnel
minikube tunnel
```

---

## Success Criteria

1. **Containerization**
   - [ ] Frontend Docker image builds successfully
   - [ ] Backend Docker image builds successfully
   - [ ] Images are optimized (multi-stage builds)
   - [ ] Health checks configured

2. **Kubernetes Deployment**
   - [ ] Pods running in todo namespace
   - [ ] Services accessible
   - [ ] Resource limits applied
   - [ ] Probes configured and passing

3. **Helm Charts**
   - [ ] Charts lint successfully
   - [ ] Charts install without errors
   - [ ] Values properly templated
   - [ ] Upgrades work correctly

4. **AIOps Integration**
   - [ ] Docker AI commands work
   - [ ] kubectl-ai integration functional
   - [ ] AI-assisted debugging available

5. **End-to-End**
   - [ ] Frontend accessible via browser
   - [ ] Frontend communicates with backend
   - [ ] Todo CRUD operations work
   - [ ] AI Chat functionality works

---

## File Structure

```
Phase-4/
├── specs/
│   ├── spec.md          # This file
│   ├── plan.md          # Implementation plan
│   └── tasks.md         # Task breakdown
│
├── agents/
│   ├── docker-agent/
│   │   └── skill.md     # Docker expertise
│   ├── kubernetes-agent/
│   │   └── skill.md     # K8s expertise
│   ├── helm-agent/
│   │   └── skill.md     # Helm expertise
│   └── aiops-agent/
│       └── skill.md     # AIOps expertise
│
├── docker/
│   ├── frontend/
│   │   └── Dockerfile
│   └── backend/
│       └── Dockerfile
│
├── helm-charts/
│   ├── todo-frontend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   └── todo-backend/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── k8s/
│   ├── namespace.yaml
│   └── ingress.yaml     # Optional
│
├── docker-compose.yml   # Local testing
├── CLAUDE.md            # Phase-4 specific instructions
└── README.md            # Quick start guide
```

---

## References

- Hackathon-2 PDF: Phase-4 (Page 22-23)
- Phase-3 Source: `Phase-3/frontend/` and `Phase-3/backend/`
- Docker Documentation: https://docs.docker.com
- Kubernetes Documentation: https://kubernetes.io/docs
- Helm Documentation: https://helm.sh/docs
- Minikube Documentation: https://minikube.sigs.k8s.io/docs

---

**Status**: Specification Complete
**Next**: See plan.md for implementation steps
