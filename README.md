# end-to-end-mlops 
 
This repository contains minimal runnable code, Dockerfiles, k8s manifests and CI snippets to reproduce the demo from Final-doc-mlops.pdf. 
 
## Repo layout 
end-to-end-mlops/ 
ÃÄÄ README.md 
ÃÄÄ validate_models.sh 
ÃÄÄ Jenkinsfile 
ÃÄÄ k8s/ 
³   ÃÄÄ sentiment-deployment.yaml 
³   ÃÄÄ sentiment-service.yaml 
³   ÃÄÄ fraud-deployment.yaml 
³   ÃÄÄ fraud-service.yaml 
³   ÃÄÄ rag-deployment.yaml 
³   ÀÄÄ monitoring/ 
ÃÄÄ sentiment/ 
³   ÃÄÄ train.py 
³   ÃÄÄ serve.py 
³   ÃÄÄ requirements.txt 
³   ÀÄÄ Dockerfile 
ÃÄÄ fraud/ 
³   ÃÄÄ train.py 
³   ÃÄÄ serve.py 
³   ÃÄÄ requirements.txt 
³   ÀÄÄ Dockerfile 
ÃÄÄ rag/ 
³   ÃÄÄ buildindex.py 
³   ÃÄÄ serve.py 
³   ÃÄÄ requirements.txt 
³   ÀÄÄ Dockerfile 
ÃÄÄ models/        (git-ignored; expected artifacts) 
ÃÄÄ data/          (sample CSVs) 
ÀÄÄ tests/         (pytest) 
