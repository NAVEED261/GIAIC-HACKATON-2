# Phase-5: Google Cloud GKE Deployment Guide

## Complete Production Deployment with Kubernetes + Kafka + Dapr

---

## Pre-requisites

| Tool | Required | Installation |
|------|----------|--------------|
| Google Cloud Account | Yes | https://cloud.google.com (with $300 credit) |
| gcloud CLI | Yes | https://cloud.google.com/sdk/docs/install |
| kubectl | Yes | Comes with gcloud |
| Docker Desktop | Yes | Already installed |
| Helm | Yes | https://helm.sh/docs/intro/install/ |

---

## Step-by-Step Deployment

### Step 1: Google Cloud Login

```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace with your project ID)
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config list
```

---

### Step 2: Enable Required APIs

```bash
gcloud services enable container.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

### Step 3: Create GKE Cluster

```bash
# Create Kubernetes cluster (takes 5-10 minutes)
gcloud container clusters create phase5-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-medium \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 3 \
  --disk-size 30GB

# Get cluster credentials
gcloud container clusters get-credentials phase5-cluster --zone us-central1-a
```

---

### Step 4: Install Dapr on Cluster

```bash
# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr
helm upgrade --install dapr dapr/dapr \
  --version=1.12 \
  --namespace dapr-system \
  --create-namespace \
  --wait

# Verify Dapr installation
kubectl get pods -n dapr-system
```

---

### Step 5: Configure Docker for GCR

```bash
gcloud auth configure-docker
```

---

### Step 6: Build and Push Docker Images

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build and push Backend
cd Phase-5/backend
docker build -t gcr.io/$PROJECT_ID/phase5-backend:latest .
docker push gcr.io/$PROJECT_ID/phase5-backend:latest

# Build and push Frontend
cd ../frontend
docker build -t gcr.io/$PROJECT_ID/phase5-frontend:latest .
docker push gcr.io/$PROJECT_ID/phase5-frontend:latest
```

---

### Step 7: Update Kubernetes Manifests

Edit `Phase-5/gcloud/k8s/backend.yaml` and `Phase-5/gcloud/k8s/frontend.yaml`:

Replace `PROJECT_ID` with your actual Google Cloud Project ID.

Also edit `Phase-5/gcloud/k8s/secrets.yaml`:
- Add your OpenAI API key
- Update JWT secret

---

### Step 8: Deploy to Kubernetes

```bash
cd Phase-5/gcloud

# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl apply -f k8s/secrets.yaml

# Deploy databases
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/kafka.yaml

# Wait for databases
kubectl wait --for=condition=ready pod -l app=postgres -n phase5-todo --timeout=120s
kubectl wait --for=condition=ready pod -l app=redis -n phase5-todo --timeout=60s

# Deploy Dapr components
kubectl apply -f k8s/dapr/

# Deploy applications
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

# Check pods
kubectl get pods -n phase5-todo
```

---

### Step 9: Create Ingress (Public URL)

```bash
# Reserve static IP
gcloud compute addresses create phase5-ip --global

# Get the IP
gcloud compute addresses describe phase5-ip --global

# Deploy Ingress
kubectl apply -f k8s/ingress.yaml

# Wait 2-5 minutes, then check
kubectl get ingress phase5-ingress -n phase5-todo
```

---

### Step 10: Access Your App

```bash
# Get external IP
kubectl get ingress phase5-ingress -n phase5-todo -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Your app will be available at: `http://EXTERNAL_IP`

---

## Useful Commands

### Check Status

```bash
# All pods
kubectl get pods -n phase5-todo

# All services
kubectl get svc -n phase5-todo

# Ingress status
kubectl get ingress -n phase5-todo

# Logs
kubectl logs -f deployment/backend -n phase5-todo
kubectl logs -f deployment/frontend -n phase5-todo
```

### Restart Deployments

```bash
kubectl rollout restart deployment/backend -n phase5-todo
kubectl rollout restart deployment/frontend -n phase5-todo
```

---

## Cost Management

### Check Current Usage

```bash
# View cluster cost estimate
gcloud billing accounts list
```

### Delete Everything (To Stop Charges)

```bash
# Delete Ingress and IP first
kubectl delete ingress phase5-ingress -n phase5-todo
gcloud compute addresses delete phase5-ip --global

# Delete namespace (removes all resources)
kubectl delete namespace phase5-todo

# Delete the entire cluster
gcloud container clusters delete phase5-cluster --zone us-central1-a

# Verify deletion
gcloud container clusters list
```

---

## Budget Alert Setup (Important!)

1. Go to: https://console.cloud.google.com/billing
2. Click "Budgets & alerts"
3. Create Budget:
   - Name: "Phase-5 Budget"
   - Amount: $250
   - Alert at: 50%, 90%, 100%
4. Email alerts aayengi jab budget reach hoga

---

## Estimated Monthly Cost

| Resource | Cost |
|----------|------|
| GKE Cluster | ~$72 |
| 2 Nodes (e2-medium) | ~$96 |
| Load Balancer | ~$18 |
| Storage | ~$5 |
| Network | ~$5 |
| **Total** | **~$196/month** |

**$300 Credit = ~45 days of usage**

---

## Troubleshooting

### Pods not starting

```bash
kubectl describe pod POD_NAME -n phase5-todo
kubectl logs POD_NAME -n phase5-todo
```

### Image pull errors

```bash
# Verify image exists
gcloud container images list --repository=gcr.io/YOUR_PROJECT_ID

# Re-push image
docker push gcr.io/YOUR_PROJECT_ID/phase5-backend:latest
```

### Ingress not getting IP

```bash
# Check ingress events
kubectl describe ingress phase5-ingress -n phase5-todo
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Get pods | `kubectl get pods -n phase5-todo` |
| Get logs | `kubectl logs -f deployment/backend -n phase5-todo` |
| Get IP | `kubectl get ingress -n phase5-todo` |
| Delete all | `gcloud container clusters delete phase5-cluster --zone us-central1-a` |

---

**Ready to deploy? Run the commands step by step!**
