pipeline {
    agent any

    environment {
        // Docker settings
        DOCKER_REGISTRY = "docker.io/anas974"
        IMAGE_TAG = "latest"
        DOCKER_PATH = "C:/Program Files/Docker/Docker/resources/bin/docker.exe"

        // Kubernetes settings
        KUBECTL_PATH = "C:/Program Files/Docker/Docker/resources/bin/kubectl.exe"
        KUBECONFIG = "C:/Users/mohda/.kube/config.full"
        K8S_CONTEXT = "docker-desktop"
    }

    stages {
        stage('Deploy Multiple ML Projects') {
            steps {
                script {
                    // Define all projects
                    def projects = [
                        [name: "iris", path: "ml\\iris"],
                        [name: "sentiment", path: "ml\\sentiment"],
                        [name: "fraud_churn", path: "ml\\fraud_churn"],
                        [name: "rag_chatbot", path: "ml\\rag_chatbot"]
                    ]

                    // Loop through each project
                    for (proj in projects) {
                        echo "=============================="
                        echo "🚀 Deploying ${proj.name}..."
                        echo "=============================="

                        // Build Docker image
                        bat "\"%DOCKER_PATH%\" build -t %DOCKER_REGISTRY%/${proj.name}:%IMAGE_TAG% ${proj.path}"

                        // Push Docker image
                        bat "\"%DOCKER_PATH%\" push %DOCKER_REGISTRY%/${proj.name}:%IMAGE_TAG%"

                        // Deploy to Kubernetes
                        bat "\"%KUBECTL_PATH%\" apply -f ${proj.path}\\k8s\\deployment.yml --kubeconfig=%KUBECONFIG% --context=%K8S_CONTEXT%"
                        bat "\"%KUBECTL_PATH%\" apply -f ${proj.path}\\k8s\\service.yml --kubeconfig=%KUBECONFIG% --context=%K8S_CONTEXT%"

                        // Optional: Validate deployment
                        bat "\"%KUBECTL_PATH%\" get pods -l app=${proj.name} --kubeconfig=%KUBECONFIG% --context=%K8S_CONTEXT%"
                        bat "\"%KUBECTL_PATH%\" get svc ${proj.name} --kubeconfig=%KUBECONFIG% --context=%K8S_CONTEXT%"

                        echo "✅ ${proj.name} deployed successfully!"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "🎉 All projects deployed successfully!"
        }
        failure {
            echo "❌ Pipeline failed! Check logs for errors."
        }
    }
}
