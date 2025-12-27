# Phase-4: Local Kubernetes Deployment

**Status**: **DEPLOYED ✅**

Deploy Phase-3 Todo Chatbot on local Kubernetes cluster using Minikube, Helm Charts, and AI-assisted DevOps tools.

## Quick Start

### Prerequisites
- Docker Desktop v28.3.2+ (RUNNING)
- Minikube v1.37.0+ (RUNNING)
- Helm 3.x
- kubectl CLI

### Verify Environment
```bash
# Check Docker
docker --version

# Check Minikube
minikube status

# Check kubectl
kubectl version --client
```

### Build Docker Images
```bash
cd "D:\PIAIC HACKATON PRACTICE\GIAIC-HACKATON-2"

# Build frontend
docker build -t todo-frontend:v1 -f Phase-4/docker/frontend/Dockerfile .

# Build backend
docker build -t todo-backend:v1 -f Phase-4/docker/backend/Dockerfile .
```

### Load Images to Minikube
```bash
minikube image load todo-frontend:v1
minikube image load todo-backend:v1
```

### Deploy with Helm
```bash
# Create namespace
kubectl apply -f Phase-4/k8s/namespace.yaml

# Deploy backend (set your API keys)
helm install todo-backend ./Phase-4/helm-charts/todo-backend -n todo \
  --set secrets.anthropicApiKey=$ANTHROPIC_API_KEY \
  --set secrets.openaiApiKey=$OPENAI_API_KEY

# Deploy frontend
helm install todo-frontend ./Phase-4/helm-charts/todo-frontend -n todo
```

### Access Application
```bash
# Get frontend URL
minikube service todo-frontend-service -n todo --url

# Get backend URL
minikube service todo-backend-service -n todo --url
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Containerization | Docker | Package applications |
| Orchestration | Kubernetes (Minikube) | Container orchestration |
| Package Manager | Helm Charts | K8s package management |
| AI DevOps | kubectl-ai, Docker AI | AI-assisted operations |

## Project Structure

```
Phase-4/
├── specs/
│   ├── spec.md          # Specification
│   ├── plan.md          # Implementation plan
│   └── tasks.md         # Task breakdown
│
├── agents/              # AI SubAgents
│   ├── docker-agent/
│   ├── kubernetes-agent/
│   ├── helm-agent/
│   └── aiops-agent/
│
├── docker/
│   ├── frontend/
│   │   └── Dockerfile   # Multi-stage Next.js build
│   └── backend/
│       ├── Dockerfile   # Optimized FastAPI build
│       └── requirements.txt
│
├── helm-charts/
│   ├── todo-frontend/   # Frontend Helm chart
│   └── todo-backend/    # Backend Helm chart
│
├── k8s/
│   ├── namespace.yaml   # Todo namespace
│   ├── frontend-deployment.yaml
│   └── backend-deployment.yaml
│
├── docker-compose.yml   # Local testing
├── CLAUDE.md            # Claude Code instructions
└── README.md            # This file
```

## Current Progress

### Completed ✅
- [x] Specifications (spec.md, plan.md, tasks.md)
- [x] SubAgent skill documentation (4 agents)
- [x] Frontend Dockerfile (multi-stage build)
- [x] Backend Dockerfile (optimized Python)
- [x] Docker Compose for local testing
- [x] Helm Charts (frontend & backend)
- [x] Kubernetes namespace manifest
- [x] Docker images built successfully
- [x] Images loaded to Minikube
- [x] Deployed with Helm
- [x] All pods running (2 frontend, 2 backend)
- [x] Services accessible via NodePort

### Pending
- [ ] Test end-to-end functionality in browser
- [ ] AIOps integration testing (optional)

## Docker Images

Verified images built:
```
todo-frontend:v1   (1.35GB)
todo-backend:v1    (474MB)
```

## Helm Charts Configuration

### Frontend (NodePort 30080)
- Replicas: 2
- Port: 3000
- Resources: 100m-500m CPU, 128Mi-512Mi Memory

### Backend (NodePort 30800)
- Replicas: 2
- Port: 8000
- Resources: 100m-500m CPU, 256Mi-512Mi Memory
- Secrets: API keys passed via Helm --set

## Troubleshooting

### Common Commands
```bash
# Check pods
kubectl get pods -n todo

# View logs
kubectl logs -f <pod-name> -n todo

# Describe pod
kubectl describe pod <pod-name> -n todo

# Delete and recreate
helm uninstall todo-frontend -n todo
helm uninstall todo-backend -n todo
```

### Image Loading
```bash
# Verify images in Minikube
minikube image list | grep todo

# Re-load if needed
minikube image load todo-frontend:v1
minikube image load todo-backend:v1
```

## References

- Hackathon-2 PDF: Phase-4 (Page 22-23)
- Phase-3 Source: `../Phase-3/frontend/` and `../Phase-3/backend/`
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs)
- [Helm Documentation](https://helm.sh/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs)

## Deployment Status

```
$ kubectl get pods -n todo
NAME                             READY   STATUS    RESTARTS   AGE
todo-backend-5d46c84fbd-j42ng    1/1     Running   0          5m
todo-backend-5d46c84fbd-v5rjw    1/1     Running   0          5m
todo-frontend-6598f6b59f-frcd2   1/1     Running   0          5m
todo-frontend-6598f6b59f-skzqq   1/1     Running   0          5m

$ kubectl get services -n todo
NAME                    TYPE       CLUSTER-IP      PORT(S)          AGE
todo-backend-service    NodePort   10.110.240.4    8000:30800/TCP   5m
todo-frontend-service   NodePort   10.108.117.88   80:30080/TCP     5m
```

---

**Next Steps**: Open frontend URL in browser and test the application!
