pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
                bat "docker build -t fitness_logger:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    '''
                }
            }
        }

        stage('Push Docker Image to Dockerhub') {
            steps {
                echo "Pushing Docker image to Dockerhub..."
                // Correct tag format: username/repo:tag
                bat "docker tag fitness_logger:v1 dhanihaneesha/fitness_logger:v1"
                bat "docker push dhanihaneesha/fitness_logger:v1"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
        stage('Restart Deployment') {
            steps {
                echo "Restarting Deployment to pick up new image..."
                bat "kubectl rollout restart deployment/fitness-deployment"
            }
        }

    }
}
