pipeline {
  agent any
  triggers {
    pollSCM('H/15 * * * *')
  }
  stages {
    stage('Build Container') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker build -t raspi_cpu ."
      }
    }
    stage('Tag Container') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker tag raspi_cpu fx8350:5000/raspi_cpu:latest"
        sh "docker tag raspi_cpu fx8350:5000/raspi_cpu:${env.BUILD_NUMBER}"
        sh "docker tag raspi_cpu leonhess/raspi_cpu:latest"
        sh "docker tag raspi_cpu leonhess/raspi_cpu:${env.BUILD_NUMBER}"
      }
    }
    stage('Push to Registries') {
      parallel {
        stage('Push to local Registry') {
          agent {
            label "Pi_3"
          }
          steps {
            sh "docker push fx8350:5000/raspi_cpu:${env.BUILD_NUMBER}"
            sh "docker push fx8350:5000/raspi_cpu:latest"
          }
        }
        stage('Push to DockerHub') {
          agent {
            label "Pi_3"
          }
          steps {
            withDockerRegistry([credentialsId: "dockerhub", url: ""]) {
              sh "docker push leonhess/raspi_cpu:${env.BUILD_NUMBER}"
              sh "docker push leonhess/raspi_cpu:latest"
            }
          }
        }
      }
    }
    stage('Cleanup') {
      agent {
        label "Pi_3"
      }
      steps {
        sh "docker rmi fx8350:5000/raspi_cpu:latest"
        sh "docker rmi fx8350:5000/raspi_cpu:${env.BUILD_NUMBER}"
        sh "docker rmi leonhess/raspi_cpu:latest"
        sh "docker rmi leonhess/raspi_cpu:${env.BUILD_NUMBER}"
      }
    }
    stage('Deploy to leon-raspi-cluster-3') {
      agent {
        label "master"
      }
      steps {
        ansiblePlaybook(
          playbook: 'deploy.yml',
          credentialsId: 'd4eb3f5d-d0f5-4964-8bad-038f0d774551'
          )
        }
      }
    }
  }
