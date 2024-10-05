pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'NotesApp.settings'
        PYTHONPATH = "/usr/src/app"
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t mynotes:latest .'  // Build Docker image
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag mynotes:latest melbinmanoj/mynotes:latest'  // Tag the image
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'dockertoken', variable: 'DOCKER_TOKEN')]) {
                        sh '''
                        echo "$DOCKER_TOKEN" | docker login -u melbinmanoj --password-stdin
                        docker push melbinmanoj/mynotes:latest
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("melbinmanoj/mynotes:latest").inside {
                        sh 'pytest --ds=NotesApp.settings'  // Run tests with Django settings
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['my-ec2-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@3.85.23.96 << 'EOF'
                    cd /var/lib/jenkins/workspace/myfirstpipeline

                    # Create an .env file with necessary environment variables
                    echo "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" > .env
                    echo "DATABASE_URL=$DATABASE_URL" >> .env
                    echo "OTHER_ENV_VAR=$OTHER_ENV_VAR" >> .env

                    # Stop and remove any running containers
                    docker-compose down || true

                    # Pull the latest image from Docker Hub
                    docker pull melbinmanoj/mynotes:latest

                    # Run the containers with the latest image and environment variables
                    docker-compose up -d --remove-orphans
EOF
                    '''
                }
            }
        }
    }
}
