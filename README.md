# 🚀 ml-ops — End-to-End MLOps Project  
**Sentiment Analysis | Fraud Detection | RAG Chatbot**

This project demonstrates a **complete Machine Learning Operations (MLOps)** pipeline — from **training → containerization → deployment → monitoring → CI/CD** — using **Docker**, **Kubernetes**, **AWS (ECR + EKS)**, **Jenkins**, and **Prometheus/Grafana**.

---

## 🧭 Table of Contents
- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Prerequisites](#prerequisites)
- [Local Quickstart](#local-quickstart)
- [Deploy on Kubernetes (Minikube & EKS)](#deploy-on-kubernetes-minikube--eks)
- [AWS ECR + EKS Setup](#aws-ecr--eks-setup)
- [Jenkins CI/CD Pipeline](#jenkins-cicd-pipeline)
- [Monitoring (Prometheus + Grafana)](#monitoring-prometheus--grafana)
- [MLflow Integration](#mlflow-integration)
- [RAG & Vector DB Setup](#rag--vector-db-setup)
- [Secrets & Config](#secrets--config)
- [Validation & Testing](#validation--testing)
- [Beginner’s Completion Checklist](#beginners-completion-checklist)

---

## 📘 Project Overview
**Goal:** Build and deploy 3 ML services as microservices with unified monitoring and CI/CD:
| Service | Port | Description |
|----------|------|-------------|
| 🗣️ Sentiment Analysis | 8000 | Predicts text sentiment (positive/negative) |
| 💳 Fraud Detection | 8001 | Predicts fraud/churn from numeric input |
| 🤖 RAG Chatbot | 8002 | Retrieval-Augmented Chatbot with FAISS/Vector DB |

Each service:
- Has its own **train.py**, **serve.py**, **Dockerfile**
- Exposes FastAPI endpoints: `/health` and `/predict` (or `/query` for RAG)
- Is deployed on Kubernetes (locally or AWS EKS)
- Is validated automatically via `validate_models.sh`

---

## 📂 Folder Structure

ml-ops/
|-- README.md
|-- validate_models.sh
|-- Jenkinsfile
|-- k8s/
| |-- sentiment-deployment.yaml
| |-- sentiment-service.yaml
| |-- fraud-deployment.yaml
| |-- fraud-service.yaml
| |-- rag-deployment.yaml
| |-- rag-service.yaml
| -- monitoring/ | |-- prometheus-servicemonitor.yaml | -- grafana-dashboard.json
|-- sentiment/
| |-- train.py
| |-- serve.py
| |-- requirements.txt
| -- Dockerfile |-- fraud/ | |-- train.py | |-- serve.py | |-- requirements.txt | -- Dockerfile
|-- rag/
| |-- buildindex.py
| |-- serve.py
| |-- requirements.txt
| -- Dockerfile |-- data/ | |-- sentiment_train.csv | -- fraud_train.csv
|-- models/ (git-ignored; runtime artifacts)
-- scripts/ -- helpers.sh

---

## ⚙️ Prerequisites
Make sure these tools are installed:

| Tool | Purpose |
|------|----------|
| Docker | Containerization |
| Python 3.10+ | Training scripts |
| kubectl | Manage Kubernetes |
| minikube / Docker Desktop | Local K8s cluster |
| helm | Install Prometheus/Grafana |
| awscli + eksctl | AWS ECR/EKS setup |
| Jenkins | CI/CD pipeline |
| jq | Parse validation results |

Verify installation:
```bash
docker --version
kubectl version --client
helm version
minikube start --driver=docker --memory=8192 --cpus=2


🧩 Local Quickstart
1️⃣ Clone the Repo

git clone https://github.com/OP-CODER/ml-ops.git
cd ml-ops

2️⃣ Train Models

python sentiment/train.py --output models/sentiment.pkl
python fraud/train.py --output models/fraud.pkl
python rag/buildindex.py --data data/docs/ --out index/

3️⃣ Build Docker Images

docker build -t sentiment:local ./sentiment
docker build -t fraud:local ./fraud
docker build -t rag:local ./rag

4️⃣ Run Containers Locally

docker run -d -p 8000:8000 sentiment:local
docker run -d -p 8001:8001 fraud:local
docker run -d -p 8002:8002 rag:local

Check endpoints:

http://localhost:8000/docs

http://localhost:8001/docs

http://localhost:8002/docs

5️⃣ Validate All Services

chmod +x validate_models.sh
./validate_models.sh

☸️ Deploy on Kubernetes (Minikube & EKS)
🧱 Apply Manifests

kubectl apply -f k8s/sentiment-deployment.yaml
kubectl apply -f k8s/fraud-deployment.yaml
kubectl apply -f k8s/rag-deployment.yaml

🔍 Access via Port-Forward

kubectl port-forward deployment/sentiment-deployment 8000:8000
kubectl port-forward deployment/fraud-deployment 8001:8001
kubectl port-forward deployment/rag-deployment 8002:8002

☁️ AWS ECR + EKS Setup
1️⃣ Push Images to ECR

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
docker tag sentiment:local <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ml-ops-sentiment:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ml-ops-sentiment:latest

2️⃣ Create EKS Cluster

eksctl create cluster --name ml-demo --nodes 2 --region us-east-1

3️⃣ Deploy to EKS

kubectl apply -f k8s/
kubectl get pods -A

🧪 Jenkins CI/CD Pipeline

Stages:

Checkout

Test (pytest)

Build Docker images

Push to ECR

Deploy to EKS

Sample pipeline included in Jenkinsfile.

Setup Jenkins credentials:

docker-registry-creds → ECR username/password

Jenkins agent with Docker + kubectl

Trigger pipeline on:

Push to main

Manual job start

📊 Monitoring (Prometheus + Grafana)

Deploy monitoring stack:

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
helm install grafana grafana/grafana -n monitoring

Add scrape annotations in each deployment:

metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"


Open Grafana dashboards → visualize latency, accuracy, and API uptime.

📘 MLflow Integration

Local:

mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 --port 5000

Production:

Backend: PostgreSQL on RDS

Artifact store: S3 bucket

Deploy MLflow in K8s (Deployment + Service + PVC)

Track models from train.py:

import mlflow
mlflow.log_param("model_type", "logreg")
mlflow.sklearn.log_model(model, "sentiment_model")

🧠 RAG & Vector DB Setup

Local → FAISS
Production → Qdrant / Weaviate / Pinecone

Include:

Helm chart or YAML for vector DB

Secrets for API keys

Backup strategy using PVC or S3 snapshot

🔒 Secrets & Config

Example:

kubectl create secret generic aws-credentials \
  --from-literal=AWS_ACCESS_KEY_ID=xxx \
  --from-literal=AWS_SECRET_ACCESS_KEY=yyy

ConfigMap:

apiVersion: v1
kind: ConfigMap
metadata:
  name: sentiment-config
data:
  MODEL_PATH: "/models/sentiment.pkl"

✅ Validation & Testing

Run validation script:

./validate_models.sh

CI Integration:
In Jenkins:

stage('Test') {
  steps {
    sh 'pytest -q || (echo "Tests failed" && exit 1)'
  }
}


🧾 Beginner’s Completion Checklist

 train.py, serve.py, buildindex.py exist & run

 Dockerfile for each service

 k8s/*.yaml manifests ready

 validate_models.sh works

 Jenkins pipeline configured

 Prometheus/Grafana running

 MLflow integrated

 Sample data + models included

 Secrets created via kubectl

 Cloud (EKS) deployment tested

🎯 Congrats!
You’ve built a production-style, end-to-end MLOps pipeline that covers:

training → containerization → deployment → monitoring → CI/CD → scaling → observability.

Keep extending with:

MLflow registry

Feature store (Feast)

Auto-scaling (HPA)

Retraining triggers with Jenkins


---

That’s it ✅  
This `README.md` will render beautifully with emojis, headings, code blocks, and tables on GitHub.

Would you like me to generate the **next step** (the ready-to-paste missing minimal files for each folder: `train.py`, `serve.py`, `Dockerfile`, and manifests)?  
That would make your repo fully runnable and TL-ready.

