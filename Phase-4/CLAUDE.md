# Phase-4: Claude Code Instructions

## Phase Overview

**Phase-4**: Kubernetes Deployment of Phase-3 Todo Chatbot
**Technology**: Docker, Minikube, Helm Charts, AIOps Tools

---

## Agent Instructions

### When Working on Phase-4:

1. **Read specs first**:
   ```bash
   cat Phase-4/specs/spec.md
   cat Phase-4/specs/plan.md
   cat Phase-4/specs/tasks.md
   ```

2. **Reference SubAgent expertise**:
   - Docker operations: `Phase-4/agents/docker-agent/skill.md`
   - Kubernetes ops: `Phase-4/agents/kubernetes-agent/skill.md`
   - Helm charts: `Phase-4/agents/helm-agent/skill.md`
   - AIOps: `Phase-4/agents/aiops-agent/skill.md`

3. **Follow Hackathon-2 context**: All work must align with PDF Phase-4 requirements

---

## Quick Commands

### Build Docker Images
```bash
cd D:/PIAIC HACKATON PRACTICE/GIAIC-HACKATON-2

# Build frontend
docker build -t todo-frontend:v1 -f Phase-4/docker/frontend/Dockerfile .

# Build backend
docker build -t todo-backend:v1 -f Phase-4/docker/backend/Dockerfile .
```

### Load to Minikube
```bash
minikube image load todo-frontend:v1
minikube image load todo-backend:v1
```

### Deploy with Helm
```bash
# Create namespace
kubectl apply -f Phase-4/k8s/namespace.yaml

# Install backend
helm install todo-backend ./Phase-4/helm-charts/todo-backend -n todo \
  --set secrets.anthropicApiKey=$ANTHROPIC_API_KEY \
  --set secrets.openaiApiKey=$OPENAI_API_KEY

# Install frontend
helm install todo-frontend ./Phase-4/helm-charts/todo-frontend -n todo
```

### Access Application
```bash
minikube service todo-frontend-service -n todo --url
minikube service todo-backend-service -n todo --url
```

---

## File References

| File | Purpose |
|------|---------|
| `specs/spec.md` | Complete Phase-4 specification |
| `specs/plan.md` | Implementation plan |
| `specs/tasks.md` | Task breakdown |
| `agents/*/skill.md` | Domain expertise |
| `docker/frontend/Dockerfile` | Frontend container |
| `docker/backend/Dockerfile` | Backend container |
| `helm-charts/todo-frontend/` | Frontend Helm chart |
| `helm-charts/todo-backend/` | Backend Helm chart |
| `k8s/namespace.yaml` | Kubernetes namespace |
| `docker-compose.yml` | Local testing |

---

## SubAgents

Each domain has a dedicated SubAgent with documented expertise:

1. **Docker Agent** - Containerization
2. **Kubernetes Agent** - K8s operations
3. **Helm Agent** - Package management
4. **AIOps Agent** - AI-assisted DevOps

---

## Important Notes

- All Phase-4 work is under `Phase-4/` folder
- History recorded in `history/prompts/phase-4/`
- Follow Hackathon-2 PDF context strictly
- Environment: Docker v28.3.2, Minikube v1.37.0 (RUNNING)
