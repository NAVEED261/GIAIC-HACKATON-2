@echo off
REM ============================================
REM Phase-5 Google Cloud GKE Deployment Script
REM For Windows Users
REM ============================================

echo ========================================
echo   Phase-5 GKE Deployment Script
echo ========================================

REM Configuration - UPDATE THESE VALUES
set PROJECT_ID=your-project-id
set CLUSTER_NAME=phase5-cluster
set ZONE=us-central1-a

REM Step 1: Set Project
echo.
echo Step 1: Setting GCP Project...
call gcloud config set project %PROJECT_ID%

REM Step 2: Enable Required APIs
echo.
echo Step 2: Enabling APIs...
call gcloud services enable container.googleapis.com
call gcloud services enable containerregistry.googleapis.com
call gcloud services enable cloudbuild.googleapis.com

REM Step 3: Create GKE Cluster
echo.
echo Step 3: Creating GKE Cluster (this takes 5-10 minutes)...
call gcloud container clusters create %CLUSTER_NAME% --zone %ZONE% --num-nodes 2 --machine-type e2-medium --enable-autoscaling --min-nodes 1 --max-nodes 3 --disk-size 30GB

REM Step 4: Get Cluster Credentials
echo.
echo Step 4: Getting Cluster Credentials...
call gcloud container clusters get-credentials %CLUSTER_NAME% --zone %ZONE%

REM Step 5: Install Dapr
echo.
echo Step 5: Installing Dapr...
call helm repo add dapr https://dapr.github.io/helm-charts/
call helm repo update
call helm upgrade --install dapr dapr/dapr --version=1.12 --namespace dapr-system --create-namespace --wait

REM Step 6: Configure Docker for GCR
echo.
echo Step 6: Configuring Docker...
call gcloud auth configure-docker

REM Step 7: Build and Push Backend
echo.
echo Step 7: Building Backend Image...
cd ..\backend
call docker build -t gcr.io/%PROJECT_ID%/phase5-backend:latest .
call docker push gcr.io/%PROJECT_ID%/phase5-backend:latest

REM Step 8: Build and Push Frontend
echo.
echo Step 8: Building Frontend Image...
cd ..\frontend
call docker build -t gcr.io/%PROJECT_ID%/phase5-frontend:latest .
call docker push gcr.io/%PROJECT_ID%/phase5-frontend:latest

cd ..\gcloud

REM Step 9: Apply Kubernetes Manifests
echo.
echo Step 9: Deploying to Kubernetes...
call kubectl apply -f k8s\namespace.yaml
call kubectl apply -f k8s\secrets.yaml
call kubectl apply -f k8s\postgres.yaml
call kubectl apply -f k8s\redis.yaml
call kubectl apply -f k8s\kafka.yaml

echo.
echo Waiting 60 seconds for databases...
timeout /t 60

REM Deploy Dapr components
call kubectl apply -f k8s\dapr\

REM Deploy applications (need to replace PROJECT_ID manually first)
echo.
echo IMPORTANT: Edit k8s\backend.yaml and k8s\frontend.yaml
echo Replace PROJECT_ID with your actual project ID: %PROJECT_ID%
echo.
pause

call kubectl apply -f k8s\backend.yaml
call kubectl apply -f k8s\frontend.yaml

REM Step 10: Create Static IP and Ingress
echo.
echo Step 10: Creating Static IP...
call gcloud compute addresses create phase5-ip --global

echo.
echo Step 11: Deploying Ingress...
call kubectl apply -f k8s\ingress.yaml

REM Wait for Ingress
echo.
echo Waiting for Ingress IP (2-5 minutes)...
timeout /t 120

echo.
echo ========================================
echo   Checking Deployment Status
echo ========================================
call kubectl get pods -n phase5-todo
call kubectl get ingress -n phase5-todo

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Run this command to get your public IP:
echo   kubectl get ingress phase5-ingress -n phase5-todo
echo.
pause
