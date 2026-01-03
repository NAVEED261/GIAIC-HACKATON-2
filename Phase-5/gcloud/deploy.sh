#!/bin/bash

# ============================================
# Phase-5 Google Cloud GKE Deployment Script
# ============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Phase-5 GKE Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"

# Configuration - UPDATE THESE VALUES
PROJECT_ID="your-project-id"
CLUSTER_NAME="phase5-cluster"
ZONE="us-central1-a"
REGION="us-central1"

# Step 1: Set Project
echo -e "\n${YELLOW}Step 1: Setting GCP Project...${NC}"
gcloud config set project $PROJECT_ID

# Step 2: Enable Required APIs
echo -e "\n${YELLOW}Step 2: Enabling APIs...${NC}"
gcloud services enable container.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Step 3: Create GKE Cluster
echo -e "\n${YELLOW}Step 3: Creating GKE Cluster...${NC}"
gcloud container clusters create $CLUSTER_NAME \
  --zone $ZONE \
  --num-nodes 2 \
  --machine-type e2-medium \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 3 \
  --disk-size 30GB

# Step 4: Get Cluster Credentials
echo -e "\n${YELLOW}Step 4: Getting Cluster Credentials...${NC}"
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

# Step 5: Install Dapr
echo -e "\n${YELLOW}Step 5: Installing Dapr...${NC}"
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm upgrade --install dapr dapr/dapr \
  --version=1.12 \
  --namespace dapr-system \
  --create-namespace \
  --wait

# Step 6: Build and Push Docker Images
echo -e "\n${YELLOW}Step 6: Building and Pushing Docker Images...${NC}"

# Backend
cd ../backend
docker build -t gcr.io/$PROJECT_ID/phase5-backend:latest .
docker push gcr.io/$PROJECT_ID/phase5-backend:latest

# Frontend
cd ../frontend
docker build -t gcr.io/$PROJECT_ID/phase5-frontend:latest .
docker push gcr.io/$PROJECT_ID/phase5-frontend:latest

cd ../gcloud

# Step 7: Update manifests with Project ID
echo -e "\n${YELLOW}Step 7: Updating manifests...${NC}"
sed -i "s|PROJECT_ID|$PROJECT_ID|g" k8s/backend.yaml
sed -i "s|PROJECT_ID|$PROJECT_ID|g" k8s/frontend.yaml

# Step 8: Apply Kubernetes Manifests
echo -e "\n${YELLOW}Step 8: Deploying to Kubernetes...${NC}"
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/kafka.yaml

# Wait for databases to be ready
echo -e "\n${YELLOW}Waiting for databases...${NC}"
kubectl wait --for=condition=ready pod -l app=postgres -n phase5-todo --timeout=120s
kubectl wait --for=condition=ready pod -l app=redis -n phase5-todo --timeout=60s

# Deploy Dapr components
kubectl apply -f k8s/dapr/

# Deploy applications
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

# Wait for applications to be ready
echo -e "\n${YELLOW}Waiting for applications...${NC}"
kubectl wait --for=condition=ready pod -l app=backend -n phase5-todo --timeout=120s
kubectl wait --for=condition=ready pod -l app=frontend -n phase5-todo --timeout=120s

# Step 9: Reserve Static IP
echo -e "\n${YELLOW}Step 9: Creating Static IP...${NC}"
gcloud compute addresses create phase5-ip --global || true

# Step 10: Deploy Ingress
echo -e "\n${YELLOW}Step 10: Deploying Ingress...${NC}"
kubectl apply -f k8s/ingress.yaml

# Step 11: Get External IP
echo -e "\n${YELLOW}Step 11: Getting External IP...${NC}"
echo "Waiting for Ingress to get an IP (this may take 2-5 minutes)..."
sleep 60

EXTERNAL_IP=$(kubectl get ingress phase5-ingress -n phase5-todo -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${GREEN}Your app is available at:${NC}"
echo -e "  http://$EXTERNAL_IP"
echo -e "\n${YELLOW}Note: It may take 5-10 minutes for the app to be fully accessible.${NC}"
echo -e "\n${YELLOW}To check status:${NC}"
echo -e "  kubectl get pods -n phase5-todo"
echo -e "  kubectl get ingress -n phase5-todo"
