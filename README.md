# ML Ops Project — Sentiment, Fraud, and RAG Services

## Overview

This repository contains three machine learning services:

1. **Sentiment Analysis** — predicts sentiment from text  
2. **Fraud Detection** — predicts fraud based on features  
3. **RAG Chatbot** — retrieves answers from a document collection  

Each service can run **locally**, in **Docker**, or on **Kubernetes**.

---

## Repo Structure

ml-ops/
├── README.md
├── validate_models.sh
├── k8s/
│   ├── sentiment-deployment.yaml
│   ├── sentiment-service.yaml
│   ├── fraud-deployment.yaml
│   ├── fraud-service.yaml
│   ├── rag-deployment.yaml
│   └── rag-service.yaml
├── sentiment/
│   ├── train.py
│   ├── serve.py
│   ├── requirements.txt
│   └── Dockerfile
├── fraud/
│   ├── train.py
│   ├── serve.py
│   ├── requirements.txt
│   └── Dockerfile
├── rag/
│   ├── buildindex.py
│   ├── serve.py
│   ├── requirements.txt
│   └── Dockerfile
├── models/       (trained models will be saved here)
└── data/         (sample CSVs or documents)

---

## Step 1 — Install Dependencies

```bash
# Sentiment
cd sentiment
pip install -r requirements.txt

# Fraud
cd ../fraud
pip install -r requirements.txt

# RAG
cd ../rag
pip install -r requirements.txt

## Step 2 — Train Models / Build Index

```bash
# Sentiment
cd sentiment
python train.py

# Fraud
cd ../fraud
python train.py

# RAG
cd ../rag
python buildindex.py

## Step 3 — Run Services Locally

```bash
# Sentiment
cd sentiment
uvicorn serve:app --host 0.0.0.0 --port 8000

# Fraud
cd ../fraud
uvicorn serve:app --host 0.0.0.0 --port 8001

# RAG
cd ../rag
uvicorn serve:app --host 0.0.0.0 --port 8002


## Step 4 — Validate All Services

```bash
# Bash (Linux/WSL/Git Bash)
bash validate_models.sh

# PowerShell (Windows)
.\validate_models.ps1

## Step 5 — Docker

```bash
docker build -t sentiment:local ./sentiment
docker build -t fraud:local ./fraud
docker build -t rag:local ./rag

docker run -d -p 8000:8000 sentiment:local
docker run -d -p 8001:8001 fraud:local
docker run -d -p 8002:8002 rag:local

## Step 6 — Kubernetes Deployment

```bash
1. Load local images into Minikube (if using Minikube):

minikube image load sentiment:local
minikube image load fraud:local
minikube image load rag:local


2. Apply Manifest

kubectl apply -f k8s/sentiment-deployment.yaml
kubectl apply -f k8s/sentiment-service.yaml
kubectl apply -f k8s/fraud-deployment.yaml
kubectl apply -f k8s/fraud-service.yaml
kubectl apply -f k8s/rag-deployment.yaml
kubectl apply -f k8s/rag-service.yaml

3. Port-Forwarding For local testing:

kubectl port-forward deployment/sentiment-deployment 8000:8000
kubectl port-forward deployment/fraud-deployment 8001:8001
kubectl port-forward deployment/rag-deployment 8002:8002

✅ You can now access the services at localhost:8000, localhost:8001, and localhost:8002.


## Step 7 — Optional: Monitoring

```bash
Prometheus can scrape /health endpoints of each service.

Grafana dashboards can visualize API latency, model accuracy, and RAG metrics.


## Step 8 — CI/CD (Optional)

```bash
Use the included Jenkinsfile for automated build, push, and deployment.

Configure credentials for Docker registry and Kubernetes cluster.

Notes

Models: models/ is git-ignored; trained models should be stored here.

Sample Data: place test CSVs or documents in data/.

Secrets/Configs: create Kubernetes secrets or ConfigMaps as needed.
