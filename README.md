# end-to-end-mlops 
 
This repository contains minimal runnable code, Dockerfiles, k8s manifests and CI snippets to reproduce the demo from Final-doc-mlops.pdf. 
 
## Repo layout 
end-to-end-mlops/ 
��� README.md 
��� validate_models.sh 
��� Jenkinsfile 
��� k8s/ 
�   ��� sentiment-deployment.yaml 
�   ��� sentiment-service.yaml 
�   ��� fraud-deployment.yaml 
�   ��� fraud-service.yaml 
�   ��� rag-deployment.yaml 
�   ��� monitoring/ 
��� sentiment/ 
�   ��� train.py 
�   ��� serve.py 
�   ��� requirements.txt 
�   ��� Dockerfile 
��� fraud/ 
�   ��� train.py 
�   ��� serve.py 
�   ��� requirements.txt 
�   ��� Dockerfile 
��� rag/ 
�   ��� buildindex.py 
�   ��� serve.py 
�   ��� requirements.txt 
�   ��� Dockerfile 
��� models/        (git-ignored; expected artifacts) 
��� data/          (sample CSVs) 
��� tests/         (pytest) 
