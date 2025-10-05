ml-ops — End-to-end MLOps (Local + AWS EKS + Jenkins CI/CD)

A beginner-friendly, full README to make your repo runnable locally (Docker / Minikube) and deployable to AWS (ECR + EKS) with Jenkins CI/CD, monitoring, MLflow guidance, RAG/vector DB notes, secrets handling, and validation steps.

Table of contents

Repo layout

Prerequisites

Local quickstart (recommended order)

train models

build RAG index

run services with Docker

run services on Minikube

validate services

Kubernetes deployment (Minikube & EKS)

manifests (examples included)

Prometheus scrape annotations / ServiceMonitor

ingress, TLS notes

AWS ECR + EKS (cloud)

Jenkins CI/CD (pipeline)

Monitoring & Logging (Prometheus, Grafana, Loki)

MLflow (experiment tracking & model registry)

RAG / Vector DB options (FAISS, Qdrant, Weaviate, Pinecone)

Secrets & config (k8s Secrets, ConfigMaps, values.yaml)

Validation, tests, and CI gates

Checklist before submission

Appendix — minimal file templates (copy/paste)


## Overview

This repository contains three machine learning services:

1. **Sentiment Analysis** — predicts sentiment from text  
2. **Fraud Detection** — predicts fraud based on features  
3. **RAG Chatbot** — retrieves answers from a document collection  

Each service can run **locally**, in **Docker**, or on **Kubernetes**.

---

## Repo Structure

```

ml-ops/
├── README.md
├── validate_models.sh
├── Jenkinsfile
├── k8s/
│   ├── sentiment-deployment.yaml
│   ├── sentiment-service.yaml
│   ├── fraud-deployment.yaml
│   ├── fraud-service.yaml
│   ├── rag-deployment.yaml
│   ├── rag-service.yaml
│   └── monitoring/
│       ├── prometheus-servicemonitor.yaml
│       └── grafana-dashboard.json
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
├── data/
│   ├── sentiment_train.csv
│   └── fraud_train.csv
├── models/        (gitignored; expected runtime artifacts)
└── scripts/
    └── helpers.sh

Prerequisites

Install locally:

Docker (desktop or engine)

kubectl

minikube (or Docker Desktop Kubernetes)

helm (v3)

Python 3.10+

awscli & eksctl (for EKS steps)

Jenkins server (for CI/CD)

(Optional) mlflow, qdrant/weaviate CLI if using vector DBs

Verify 
```
---
docker --version
kubectl version --client
helm version
minikube start --driver=docker --memory=8192 --cpus=2

Local quickstart (recommended order)

Goal: from zero → run/test endpoints locally.

```
---
1) Clone the repo

git clone https://github.com/OP-CODER/ml-ops.git
cd ml-ops

```
---
2) Create a Python venv (optional but recommended)

python -m venv .venv
source .venv/bin/activate

```
---
3) Train models locally (creates artifacts under models/)

Each service folder has a train.py that writes model files to models/. Example commands:

Sentiment:
python sentiment/train.py --output models/sentiment.pkl

Fraud:
python fraud/train.py --output models/fraud.pkl

RAG index:
python rag/buildindex.py --data data/docs/ --out index/

If you don't have sample data yet, see data/ in the repo for example CSVs. If training will take long you can include prebuilt small models under models/ (gitignored recommended — but for a demo, include tiny toy models).

```
---

4) Build Docker images (local sanity)

Each service has a Dockerfile. Run:
docker build -t sentiment:local ./sentiment
docker build -t fraud:local ./fraud
docker build -t rag:local ./rag

```
---

5) Run services locally

docker run -d -p 8000:8000 --name sentiment_local sentiment:local
docker run -d -p 8001:8001 --name fraud_local fraud:local
docker run -d -p 8002:8002 --name rag_local rag:local

Open:

Sentiment: http://localhost:8000/docs

Fraud: http://localhost:8001/docs

RAG: http://localhost:8002/docs

```
---

6) Validate with validate_models.sh

Make script executable and run:
chmod +x validate_models.sh
./validate_models.sh

Expect JSON responses. The script should return non-zero exit codes on failure and write validation_results.txt.

```
---

Kubernetes deployment (Minikube & EKS)
1) For Minikube (quick local k8s)

Load local image into minikube (or push to a registry):
minikube image load sentiment:local
minikube image load fraud:local
minikube image load rag:local

Apply manifests:

kubectl apply -f k8s/sentiment-deployment.yaml
kubectl apply -f k8s/sentiment-service.yaml
kubectl apply -f k8s/fraud-deployment.yaml
kubectl apply -f k8s/fraud-service.yaml
kubectl apply -f k8s/rag-deployment.yaml
kubectl apply -f k8s/rag-service.yaml


Port-forward to access:

kubectl port-forward deployment/sentiment-deployment 8000:8000
kubectl port-forward deployment/fraud-deployment 8001:8001
kubectl port-forward deployment/rag-deployment 8002:8002

```
---

2) Manifests (minimal example snippets are in Appendix)

Ensure each Deployment template includes readinessProbe and prometheus scrape annotations (or provide a ServiceMonitor).

Provide PVC definitions in k8s/ if you use persistent storage (e.g., for FAISS indexes or MLflow artifacts).

3) Prometheus scraping
Two approaches:

Pod template annotations (prometheus.io/scrape: "true") — quick and easy.

ServiceMonitor manifest (recommended if using Prometheus Operator).

Example (annotation approach) is included in Deployment templates in Appendix.

```
---

4) Ingress & TLS

For Minikube: use minikube tunnel or port-forward.

For production (EKS): add an Ingress manifest and use cert-manager + ClusterIssuer for TLS. Provide example Ingress YAML in k8s/.

```
---
AWS ECR + EKS (cloud)
1) Build, tag, and push images to ECR
# login (example)
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com

# create repo (if not exists)
aws ecr create-repository --repository-name ml-ops/sentiment

# tag and push
docker tag sentiment:local <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/ml-ops/sentiment:latest
docker push <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/ml-ops/sentiment:latest
# repeat for fraud and rag

2) Create EKS cluster (high-level)
eksctl create cluster --name ml-demo --nodes 2 --node-type t3.medium --region <region>

(Adjust node counts/types as needed.)

3) Update k8s manifests to use ECR images

Replace image fields in your k8s/* YAMLs with the pushed ECR image tags.

4) Expose services publicly

Use LoadBalancer service type or Ingress + ALB Ingress Controller (recommended).

Use cert-manager for TLS.
