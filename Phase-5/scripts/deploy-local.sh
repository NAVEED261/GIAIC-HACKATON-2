#!/bin/bash
# Phase-5 Local Deployment Script
# Deploys to Minikube with Dapr

set -e

echo "=========================================="
echo "  Phase-5 Local Deployment"
echo "  Minikube + Dapr + Redpanda"
echo "=========================================="

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v minikube &> /dev/null; then
    echo "ERROR: minikube not found. Please install minikube."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "ERROR: kubectl not found. Please install kubectl."
    exit 1
fi

if ! command -v dapr &> /dev/null; then
    echo "ERROR: dapr CLI not found. Please install dapr."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "ERROR: helm not found. Please install helm."
    exit 1
fi

echo "All prerequisites found!"

# Step 1: Start Minikube
echo ""
echo "Step 1: Starting Minikube..."
minikube status || minikube start --driver=docker --cpus=4 --memory=8g

# Step 2: Enable addons
echo ""
echo "Step 2: Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Step 3: Initialize Dapr
echo ""
echo "Step 3: Initializing Dapr on Kubernetes..."
dapr init -k --wait

# Step 4: Create namespace
echo ""
echo "Step 4: Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Step 5: Deploy Redpanda
echo ""
echo "Step 5: Deploying Redpanda..."
helm repo add redpanda https://charts.redpanda.com
helm repo update
helm upgrade --install redpanda redpanda/redpanda \
  --namespace todo-phase5 \
  --set statefulset.replicas=1 \
  --set resources.cpu.cores=0.5 \
  --set resources.memory.container.max=512Mi \
  --wait

# Step 6: Deploy infrastructure
echo ""
echo "Step 6: Deploying infrastructure..."
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml

# Wait for infrastructure
echo "Waiting for infrastructure to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n todo-phase5 --timeout=120s
kubectl wait --for=condition=ready pod -l app=redis -n todo-phase5 --timeout=120s

# Step 7: Apply Dapr components
echo ""
echo "Step 7: Applying Dapr components..."
kubectl apply -f backend/dapr_components/

# Step 8: Create Kafka topics
echo ""
echo "Step 8: Creating Kafka topics..."
kubectl exec -it redpanda-0 -n todo-phase5 -- rpk topic create task-events --partitions 3 || true
kubectl exec -it redpanda-0 -n todo-phase5 -- rpk topic create reminders --partitions 1 || true
kubectl exec -it redpanda-0 -n todo-phase5 -- rpk topic create notifications --partitions 1 || true

# Step 9: Build and deploy applications
echo ""
echo "Step 9: Building application images..."
eval $(minikube docker-env)
docker build -t todo-backend:phase5 -f backend/Dockerfile backend/
docker build -t todo-frontend:phase5 -f frontend/Dockerfile frontend/
docker build -t todo-notification:phase5 -f notification-service/Dockerfile notification-service/

echo ""
echo "Step 10: Deploying applications..."
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/notification-service.yaml

# Wait for applications
echo "Waiting for applications to be ready..."
kubectl wait --for=condition=ready pod -l app=backend -n todo-phase5 --timeout=180s
kubectl wait --for=condition=ready pod -l app=frontend -n todo-phase5 --timeout=180s

# Step 11: Start tunnel for LoadBalancer
echo ""
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
echo ""
echo "To access the application, run:"
echo "  minikube tunnel"
echo ""
echo "Then open:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo ""
echo "Check status:"
echo "  kubectl get pods -n todo-phase5"
echo "  dapr status -k"
echo ""
