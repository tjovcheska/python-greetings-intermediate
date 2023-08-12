pipeline {
    agent any
    triggers {
        pollSCM('*/1 * * * *')
    }
    environment {
        DOCKER_USERNAME = credentials('docker-username')
        DOCKER_PASSWORD = credentials('docker-password')
    }
    stages {
        stage('build-app') {
            steps {
                script {
                    echo "Build ${GIT_COMMIT}"
                    echo "Build python-greetings-app"
                    build("teodorajovcheska7/python-greetings-app:${GIT_COMMIT}" , "Dockerfile")
                }
            }
        }
        stage('deploy-dev') {
            steps {
                script {
                    deploy("dev")
                }
            }
        }
        stage('test-dev') {
            steps {
                script {
                    test("dev")
                }
            }
        }
        stage('approval') {
            steps {
                echo "Manual approval before deployment to PROD"
            }
        }

        stage('deploy-prod') {
            steps {
                script {
                    deploy("prod")
                }
            }
        }
        stage('test-prod') {
            steps {
                script {
                    test("prod")
                }
            }
        }
    }
    post {
        failure {
            script {
                echo "Pipeline failure... Sending notification"
                //invoce discord plugin
            }
        }
        cleanup {
            echo "Cleanup procedure..."
            //potentually some docker clean up here as well
        }
    }
}

def build(String type, String dockerfile) {
    echo "Building ${tag} image based on ${dockerfile}"
    sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
    sh "docker build --no-cache -t ${tag} . -f ${dockerfile}"
    sh "docker push ${tag}"
}

def test(String test_environment) {
    echo "Testing of python-greetings-app on ${test_environment} is starting..."
    sh "docker run --network=host -t -d --name api_tests_runner_${test_environment} teodorajovcheska7/api-tests-runner:latest"
    sh "docker exec api_tests_runner_${test_environment} cucumber PLATFORM=${test_environment} --format html --out test-output/report.html"
    sh "docker cp api_tests_runner_${test_environment}:/api-tests/test-output/report.html report_${test_environment}.html"
    sh "docker rm -f api_tests_runner_${test_environment}"
}

def deploy(String deploy_environment){
    echo "Deployment of python-greetings-app on ${deploy_environment} is starting.."
    sh "kubectl set image deployment python-greetings-${deploy_environment} python-greetings-${deploy_environment}-pod=teodorajovcheska7/python-greetings-app:${GIT_COMMIT}"
    sh "kubectl scale deploy python-greetings-${deploy_environment} --replicas=0"
    sh "kubectl scale deploy python-greetings-${deploy_environment} --replicas=1"
}