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

```

### Prerequisites

## Install locally:

## Docker (desktop or engine)

## kubectl

## minikube (or Docker Desktop Kubernetes)

## helm (v3)

## Python 3.10+

## awscli & eksctl (for EKS steps)

## Jenkins server (for CI/CD)

## (Optional) mlflow, qdrant/weaviate CLI if using vector DBs

## Verify
 
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

```
bash
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
 login (example)
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com

 create repo (if not exists)
aws ecr create-repository --repository-name ml-ops/sentiment

 tag and push
docker tag sentiment:local <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/ml-ops/sentiment:latest
docker push <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/ml-ops/sentiment:latest
 repeat for fraud and rag

2) Create EKS cluster (high-level)
eksctl create cluster --name ml-demo --nodes 2 --node-type t3.medium --region <region>

(Adjust node counts/types as needed.)

3) Update k8s manifests to use ECR images

Replace image fields in your k8s/* YAMLs with the pushed ECR image tags.

4) Expose services publicly

Use LoadBalancer service type or Ingress + ALB Ingress Controller (recommended).

Use cert-manager for TLS.

Jenkins CI/CD pipeline

Add Jenkinsfile at repo root. Minimal improved pipeline (example — included in Appendix):

Pipeline stages:

Checkout

Run tests (pytest)

Build images

Login to ECR

Push images

Update k8s (kubectl set image ...)

Important Jenkins configuration:

Add credentials in Jenkins:

docker-registry-creds (username/password or AWS access keys)

kubeconfig or use Jenkins agents with kubectl and proper IAM role

Ensure kubectl, docker, and aws CLIs installed on the agent.

Sample Jenkinsfile is included in Appendix — update REGISTRY, ACCOUNT_ID, region, and credentialsId.

## Monitoring & Logging (Prometheus, Grafana, Loki)

# Deploy Prometheus (via Helm) and Grafana:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
helm install grafana grafana/grafana --namespace monitoring

Ensure services expose /metrics or add scrape annotations in pod template (see Appendix deployment snippet).

Add ServiceMonitor YAMLs under k8s/monitoring/ if you use Prometheus Operator.

Include a grafana-dashboard.json under k8s/monitoring/ with panels for:

api_latency

ml_accuracy

request rate

llm_tokens_total (if applicable)

Logging:

Use Loki + promtail or ELK if you prefer. Include a minimal promtail manifest and Grafana datasource configuration for Loki.

## MLflow (experiment tracking & model registry)

# Local Quickstart:

```bash
# local postgres for backend store (example)
docker run -d --name mlflow-postgres -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=mlflow -e POSTGRES_DB=mlflow -p 5432:5432 postgres:13

# start mlflow server (local artifacts to ./mlflow_artifacts)
mlflow server --backend-store-uri postgresql://mlflow:pass@localhost:5432/mlflow --default-artifact-root file:./mlflow_artifacts --host 0.0.0.0 --port 5000

K8s / production:

Use a managed DB (RDS) as backend store.

Use S3 (or MinIO) as default-artifact-root.

Provide a k8s Deployment + Service + PVC (if using MinIO) or use S3 credentials in k8s Secrets.

Doc items to add:

k8s/mlflow-deployment.yaml

k8s/mlflow-service.yaml

values.yaml for helm (if using Helm chart for mlflow)

Add instructions in train.py to call mlflow.start_run() and mlflow.log_model().

```
---

## RAG / Vector DB options (FAISS, Qdrant, Weaviate, Pinecone)

Local dev: FAISS for simple vector store (index stored as files/PVC). Provide rag/buildindex.py which writes indexes to index/.

Production: recommend managed / networked vector DBs (Qdrant, Weaviate, Pinecone). Add:

Helm chart / manifests for Qdrant or Weaviate OR instructions for Pinecone managed service.

Sample k8s/qdrant-deployment.yaml or values.yaml.

Secrets for DB API keys / tokens.

Notes:

Keep index snapshots in S3/MinIO and use PVCs for runtime.

Add network policies and authentication to restrict access to vector DB.

```
---

## Secrets & config (k8s Secrets, ConfigMaps, values.yaml)

# Example create secret:

kubectl create secret generic aws-credentials --from-literal=AWS_ACCESS_KEY_ID=xxx --from-literal=AWS_SECRET_ACCESS_KEY=yyy -n mlops

Provide k8s/secrets-example.yaml with placeholders (do not commit secrets). Use values.yaml for Helm charts to inject secret names.
 

```
---

# ConfigMap example (for app config):

```bash
apiVersion: v1
kind: ConfigMap
metadata:
  name: sentiment-config
data:
  MODEL_PATH: "/models/sentiment.pkl"
  LOG_LEVEL: "INFO"

```
---

## Validation, tests, and CI gates

Add tests/ with pytest unit tests for preprocessors and small integration tests for endpoints.

validate_models.sh should:

curl each endpoint

assert expected fields

write validation_results.txt

exit non-zero on failures

Sample CI snippet (in Jenkinsfile):

```bash
stage('Test') {
  steps {
    sh 'pytest -q || (echo "Tests failed" && exit 1)'
  }
}


