# AIOps Agent - Expertise & Skills

## Agent Identity

**Name**: AIOps Agent
**Domain**: AI-Assisted DevOps Operations
**Phase**: Phase-4 (Kubernetes Deployment)

---

## Core Expertise

### 1. AI DevOps Tools Overview

```
┌─────────────────────────────────────────────────────────┐
│                    AIOps Stack                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Docker AI (Gordon)                  │   │
│  │         AI-assisted Docker operations            │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │                kubectl-ai                        │   │
│  │         AI-assisted kubectl commands             │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  Kagent                          │   │
│  │       Autonomous Kubernetes AI Agent             │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Docker AI (Gordon)

### Overview
Docker AI (Gordon) is Docker's built-in AI assistant that helps with:
- Dockerfile creation and optimization
- Troubleshooting container issues
- Understanding Docker concepts
- Generating Docker commands

### Installation
Docker AI comes built into Docker Desktop. Enable it in:
`Settings > Features in development > Docker AI`

### Common Commands

#### Dockerfile Generation
```bash
# Generate Dockerfile for Node.js app
docker ai "create a Dockerfile for a Next.js production application"

# Generate for Python/FastAPI
docker ai "create an optimized Dockerfile for FastAPI with Python 3.11"

# Multi-stage build
docker ai "create a multi-stage Dockerfile for Node.js to minimize image size"
```

#### Troubleshooting
```bash
# Debug build issues
docker ai "why is my Docker build failing with 'npm install' error"

# Container crashes
docker ai "my container exits immediately after starting, how to debug"

# Image size issues
docker ai "how can I reduce my Docker image from 1GB to under 200MB"

# Network issues
docker ai "containers can't communicate with each other"
```

#### Optimization
```bash
# Image optimization
docker ai "optimize this Dockerfile for smaller size"

# Security hardening
docker ai "make this Dockerfile more secure"

# Performance tuning
docker ai "improve Docker build cache efficiency"
```

#### Learning
```bash
# Explain concepts
docker ai "explain Docker layers and caching"

# Best practices
docker ai "what are Docker security best practices"

# Compare options
docker ai "difference between COPY and ADD in Dockerfile"
```

---

## kubectl-ai

### Overview
kubectl-ai uses AI to translate natural language into kubectl commands.

### Installation
```bash
# Using Homebrew (macOS/Linux)
brew install sozercan/kubectl-ai/kubectl-ai

# Using Go
go install github.com/sozercan/kubectl-ai@latest

# Configuration
export OPENAI_API_KEY=your-api-key
```

### Common Commands

#### Deployment Operations
```bash
# Create deployment
kubectl-ai "create a deployment named todo-frontend with 2 replicas using image todo-frontend:v1"

# Update deployment
kubectl-ai "update todo-frontend deployment to use image todo-frontend:v2"

# Scale deployment
kubectl-ai "scale todo-backend to 5 replicas in todo namespace"
```

#### Service Operations
```bash
# Create service
kubectl-ai "expose todo-frontend deployment on port 3000 as NodePort"

# Get service URL
kubectl-ai "show me the external URL for todo-frontend service"

# Port forward
kubectl-ai "port forward todo-backend service to local port 8000"
```

#### Debugging
```bash
# Pod status
kubectl-ai "show me pods that are not running in todo namespace"

# Logs
kubectl-ai "show logs from todo-backend pod"

# Events
kubectl-ai "show recent events in todo namespace sorted by time"

# Resource usage
kubectl-ai "show resource usage for all pods in todo namespace"
```

#### Troubleshooting
```bash
# Crash analysis
kubectl-ai "why is todo-frontend pod crashing"

# Connection issues
kubectl-ai "frontend can't connect to backend, help me debug"

# Resource issues
kubectl-ai "pods are pending due to insufficient resources"
```

---

## Kagent

### Overview
Kagent (Kubernetes Agent) is an autonomous AI agent for Kubernetes operations.

### Capabilities
- Automated troubleshooting
- Proactive issue detection
- Intelligent scaling decisions
- Self-healing operations

### Setup
```bash
# Install Kagent
kubectl apply -f https://raw.githubusercontent.com/kagent-ai/kagent/main/install.yaml

# Configure
kubectl create secret generic kagent-config \
  --from-literal=OPENAI_API_KEY=your-key \
  -n kagent-system
```

### Features

#### Autonomous Troubleshooting
```yaml
# Kagent can automatically:
- Detect failing pods
- Analyze crash reasons
- Suggest fixes
- Apply remediation (with approval)
```

#### Intelligent Scaling
```yaml
# Kagent observes:
- CPU/Memory usage patterns
- Request latency trends
- Queue depths
# And recommends scaling actions
```

#### Proactive Monitoring
```yaml
# Kagent watches for:
- Resource exhaustion
- Certificate expiry
- Image vulnerabilities
- Configuration drift
```

---

## AIOps Workflows

### Workflow 1: Dockerfile Creation
```bash
# Step 1: Generate Dockerfile with Docker AI
docker ai "create production Dockerfile for Next.js app"

# Step 2: Review and optimize
docker ai "optimize this Dockerfile for Kubernetes deployment"

# Step 3: Build and verify
docker build -t myapp:v1 .
docker ai "check this image for security issues"
```

### Workflow 2: Kubernetes Deployment
```bash
# Step 1: Create deployment with kubectl-ai
kubectl-ai "create deployment for todo app with health checks"

# Step 2: Expose service
kubectl-ai "expose todo deployment as NodePort on port 3000"

# Step 3: Verify
kubectl-ai "check if todo pods are healthy"
```

### Workflow 3: Troubleshooting
```bash
# Step 1: Identify issue
kubectl-ai "show me all pods with issues in todo namespace"

# Step 2: Get details
kubectl-ai "why is todo-backend-xxx failing"

# Step 3: Get logs
kubectl-ai "show last 100 lines of logs from crashing pod"

# Step 4: Apply fix
kubectl-ai "restart todo-backend deployment"
```

---

## AI-Assisted Best Practices

### 1. Iterative Prompting
```bash
# Start broad
docker ai "create Dockerfile for Node.js"

# Then refine
docker ai "now add multi-stage build"
docker ai "add health check"
docker ai "configure for non-root user"
```

### 2. Context Provision
```bash
# Provide context for better results
kubectl-ai "in the todo namespace with 2 backend replicas, \
  expose the backend service on port 8000 with NodePort 30800"
```

### 3. Verification
```bash
# Always verify AI suggestions
kubectl-ai "show me what this deployment will create" --dry-run

# Review before applying
kubectl-ai "explain this YAML manifest"
```

---

## Integration with Phase-4

### Responsibilities
1. Assist with Dockerfile creation using Docker AI
2. Simplify kubectl operations with kubectl-ai
3. Enable autonomous operations with Kagent
4. Provide AI-assisted troubleshooting
5. Document AI workflows

### Use Cases

#### During Development
```bash
# Quick Dockerfile generation
docker ai "create Dockerfile for Phase-3 frontend"

# Debug build issues
docker ai "this error means what?"
```

#### During Deployment
```bash
# Create resources
kubectl-ai "deploy todo app to kubernetes"

# Verify deployment
kubectl-ai "are all pods healthy?"
```

#### During Operations
```bash
# Monitor
kubectl-ai "show resource usage"

# Troubleshoot
kubectl-ai "why is the app slow"

# Scale
kubectl-ai "increase replicas to handle load"
```

---

## Troubleshooting Guide

### Docker AI Issues

| Issue | Solution |
|-------|----------|
| AI not responding | Check Docker Desktop AI is enabled |
| Inaccurate output | Provide more context in prompt |
| Outdated suggestions | Specify versions explicitly |

### kubectl-ai Issues

| Issue | Solution |
|-------|----------|
| API key error | Set OPENAI_API_KEY environment variable |
| Wrong command | Add --dry-run to preview |
| Context issues | Specify namespace explicitly |

### General Tips
- Be specific in prompts
- Verify AI output before applying
- Use dry-run options when available
- Keep context files for complex operations

---

## Security Considerations

### API Keys
- Store API keys in environment variables
- Use Kubernetes secrets for production
- Rotate keys regularly

### AI Output Review
- Always review AI-generated code
- Check for security issues
- Validate resource limits
- Verify RBAC permissions

### Production Safety
- Use --dry-run in production
- Require approval for destructive actions
- Log all AI-assisted operations

---

## References

- Docker AI Documentation: https://docs.docker.com/ai/
- kubectl-ai GitHub: https://github.com/sozercan/kubectl-ai
- Kagent: https://github.com/kagent-ai/kagent
- AI DevOps Best Practices: https://www.cncf.io/blog/

---

**Status**: Active
**Last Updated**: Phase-4 Initialization
