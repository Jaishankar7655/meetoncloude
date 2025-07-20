pipeline {
    agent {
        label 'jai'
    }

    stages {

        stage('Code') {
            steps {
                echo 'Fetching the latest code...'
                git url: 'https://github.com/Jaishankar7655/meetoncloude.git', branch: 'main'
                echo 'Code cloned successfully.'
            }
        }

        stage('Test') {
            steps {
                echo "Running tests..."
                // You can add actual test commands here later
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker containers...'
                sh 'docker compose build'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing images to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhubcred', passwordVariable: 'dockerHubpass', usernameVariable: 'dockerhubUser')]) {
                    sh 'docker login -u $dockerhubUser -p $dockerHubpass'
                    sh 'docker image tag meetoncloude_django:latest $dockerhubUser/meet-oncloude:latest'
                    sh 'docker push $dockerhubUser/meet-oncloude:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                sh 'docker compose up -d'
            }
        }

    }
}
