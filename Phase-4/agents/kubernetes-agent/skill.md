# Kubernetes Agent - Expertise & Skills

## Agent Identity

**Name**: Kubernetes Agent
**Domain**: Container Orchestration & Kubernetes Operations
**Phase**: Phase-4 (Kubernetes Deployment)

---

## Core Expertise

### 1. Kubernetes Architecture

#### Core Components
```
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                         │
│  ┌─────────────┐ ┌──────────┐ ┌────────────────────┐   │
│  │ API Server  │ │ etcd     │ │ Controller Manager │   │
│  └─────────────┘ └──────────┘ └────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Scheduler                           │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────┐
│                    Worker Nodes                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    Node 1    │  │    Node 2    │  │    Node N    │  │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │  │
│  │  │ kubelet│  │  │  │ kubelet│  │  │  │ kubelet│  │  │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │  │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │  │
│  │  │ Pods   │  │  │  │ Pods   │  │  │  │ Pods   │  │  │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2. Resource Types

#### Workloads
- **Pod**: Smallest deployable unit
- **Deployment**: Manages ReplicaSets
- **ReplicaSet**: Ensures pod replicas
- **StatefulSet**: Stateful applications
- **DaemonSet**: One pod per node
- **Job/CronJob**: Batch tasks

#### Services & Networking
- **Service**: Exposes pods
- **Ingress**: External access
- **NetworkPolicy**: Traffic rules

#### Configuration
- **ConfigMap**: Non-sensitive config
- **Secret**: Sensitive data
- **PersistentVolume**: Storage

---

## Kubernetes Manifests

### Deployment Template
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-app
  namespace: {{ .Release.Namespace }}
  labels:
    app: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.containerPort }}
          resources:
            requests:
              cpu: {{ .Values.resources.requests.cpu }}
              memory: {{ .Values.resources.requests.memory }}
            limits:
              cpu: {{ .Values.resources.limits.cpu }}
              memory: {{ .Values.resources.limits.memory }}
          livenessProbe:
            httpGet:
              path: /health
              port: {{ .Values.containerPort }}
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: {{ .Values.containerPort }}
            initialDelaySeconds: 5
            periodSeconds: 5
          envFrom:
            - configMapRef:
                name: {{ .Release.Name }}-config
```

### Service Template
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-service
  namespace: {{ .Release.Namespace }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.containerPort }}
      nodePort: {{ .Values.service.nodePort }}
  selector:
    app: {{ .Release.Name }}
```

### ConfigMap Template
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-config
  namespace: {{ .Release.Namespace }}
data:
  NODE_ENV: "production"
  API_URL: "{{ .Values.config.apiUrl }}"
```

### Secret Template
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ .Release.Name }}-secrets
  namespace: {{ .Release.Namespace }}
type: Opaque
data:
  # Base64 encoded values
  ANTHROPIC_API_KEY: {{ .Values.secrets.anthropicApiKey | b64enc }}
  OPENAI_API_KEY: {{ .Values.secrets.openaiApiKey | b64enc }}
```

---

## Minikube Operations

### Basic Commands
```bash
# Start cluster
minikube start --driver=docker

# Check status
minikube status

# Dashboard
minikube dashboard

# Get IP
minikube ip

# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

### Image Management
```bash
# Load local image
minikube image load todo-frontend:v1

# Build in Minikube
eval $(minikube docker-env)
docker build -t app:v1 .

# List images
minikube image list
```

### Service Access
```bash
# Get service URL
minikube service <service-name> -n <namespace> --url

# Tunnel for LoadBalancer
minikube tunnel

# Port forward
kubectl port-forward svc/<service-name> 3000:3000 -n <namespace>
```

---

## kubectl Commands

### Resource Management
```bash
# Create resources
kubectl apply -f manifest.yaml

# Get resources
kubectl get pods,svc,deploy -n todo

# Describe resource
kubectl describe pod <pod-name> -n todo

# Delete resources
kubectl delete -f manifest.yaml
```

### Debugging
```bash
# View logs
kubectl logs <pod-name> -n todo
kubectl logs -f <pod-name> -n todo  # Follow

# Execute in pod
kubectl exec -it <pod-name> -n todo -- sh

# Port forward
kubectl port-forward pod/<pod-name> 8080:8000 -n todo

# Get events
kubectl get events -n todo --sort-by='.lastTimestamp'
```

### Namespace Management
```bash
# Create namespace
kubectl create namespace todo

# Set default namespace
kubectl config set-context --current --namespace=todo

# List namespaces
kubectl get namespaces
```

---

## kubectl-ai Integration

### Common AI Commands
```bash
# Deploy application
kubectl-ai "deploy todo-frontend with 2 replicas using image todo-frontend:v1"

# Scale deployment
kubectl-ai "scale todo-backend to 3 replicas"

# Get pod status
kubectl-ai "show me pods that are not running in todo namespace"

# Debug issues
kubectl-ai "why is pod todo-frontend-xxx crashing"

# Create service
kubectl-ai "expose todo-backend on port 8000 as NodePort"
```

---

## Best Practices

### Resource Limits
```yaml
resources:
  requests:
    cpu: "100m"      # 0.1 CPU
    memory: "128Mi"
  limits:
    cpu: "500m"      # 0.5 CPU
    memory: "512Mi"
```

### Health Probes
```yaml
# Liveness: Is container alive?
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

# Readiness: Is container ready for traffic?
readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
  successThreshold: 1
```

### Labels & Selectors
```yaml
metadata:
  labels:
    app: todo
    component: frontend
    version: v1
    environment: production
```

---

## Troubleshooting Guide

### Pod Issues

| Status | Cause | Solution |
|--------|-------|----------|
| Pending | No resources | Check node resources |
| ImagePullBackOff | Image not found | Check image name/tag |
| CrashLoopBackOff | App crashing | Check logs |
| Error | Container error | Describe pod |
| Terminating | Stuck deletion | Force delete |

### Debug Workflow
```bash
# 1. Check pod status
kubectl get pods -n todo

# 2. Describe pod for events
kubectl describe pod <pod> -n todo

# 3. Check logs
kubectl logs <pod> -n todo

# 4. Check previous logs (if restarted)
kubectl logs <pod> -n todo --previous

# 5. Exec into pod
kubectl exec -it <pod> -n todo -- sh
```

---

## Integration with Phase-4

### Responsibilities
1. Create namespace for todo application
2. Deploy frontend and backend pods
3. Configure services for access
4. Set up health probes
5. Manage secrets and configmaps
6. Integrate with kubectl-ai

### Input from Docker Agent
- Image names and tags
- Exposed ports
- Health check endpoints
- Environment variables

### Handoff to Helm Agent
- Provide manifest templates
- Define resource requirements
- Specify service types

---

## References

- Kubernetes Documentation: https://kubernetes.io/docs
- Minikube Documentation: https://minikube.sigs.k8s.io/docs
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- kubectl-ai: https://github.com/sozercan/kubectl-ai

---

**Status**: Active
**Last Updated**: Phase-4 Initialization
