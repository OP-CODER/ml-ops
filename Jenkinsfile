pipeline {
    agent any

    environment {
        REGISTRY = "docker.io/anas974"
        IMAGE_TAG = "latest"
        KUBECONFIG = "$HOME/.kube/config"
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📦 Pulling latest code from GitHub..."
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    def projects = ["sentiment", "fraud", "rag"]
                    for (p in projects) {
                        echo "🐳 Building Docker image for ${p}..."
                        sh """
                            docker build -t ${REGISTRY}/${p}:${IMAGE_TAG} ${p}/
                        """
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-token', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${REGISTRY}/sentiment:${IMAGE_TAG}
                        docker push ${REGISTRY}/fraud:${IMAGE_TAG}
                        docker push ${REGISTRY}/rag:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Validate Models') {
            steps {
                echo "🧪 Running model validation..."
                sh "bash scripts/helpers.sh"
                sh "bash validate_models.sh"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "🚀 Applying K8s manifests..."
                sh """
                    kubectl apply -f k8s/senttiment-deployment.yml
                    kubectl apply -f k8s/senttiment-service.yml
                    kubectl apply -f k8s/fraud-deployment.yml
                    kubectl apply -f k8s/fraud-service.yml
                    kubectl apply -f k8s/rag-deployment.yml
                    kubectl apply -f k8s/rag-service.yml
                """
            }
        }

        stage('Post-Deployment Check') {
            steps {
                echo "🔍 Checking pods & services..."
                sh """
                    kubectl get pods
                    kubectl get svc
                """
            }
        }
    }

    post {
        success {
            echo "✅ All models deployed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check Jenkins logs for details."
        }
    }
}
