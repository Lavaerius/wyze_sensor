pipeline {
agent any
stages {
  /*stage('GitCheckOut') {
	steps{
	checkout([$class: 'GitSCM', branches: [[name: "${env.CHECKOUT}"]], extensions: [], userRemoteConfigs: [[credentialsId: 'gitea', url: "$GIT_URL"]]])
	}

}*/ 
 stage('buildPush') {
	steps{
	sh 'echo "ADASDASDSADSADASD"'
	sh 'docker buildx rm jenkins-agent || echo "none there"'
	sh '''#!/bin/bash 
		docker buildx create --bootstrap --name=jenkins-agent --driver=kubernetes --driver-opt=namespace=jenkinsagent --driver-opt=qemu.install=true --driver-opt=\\"nodeselector=kubernetes.io/arch=amd64\\" --driver-opt=\\"image=registry.local/buildkit-wagnerca:stable-3-rootless\\"  --use
	'''
	sh 'docker buildx build . -t registry.local/wyze_sensor:v0.0.$BUILD_NUMBER --push --platform=linux/arm64,linux/amd64'
	sh 'docker buildx rm jenkins-agent'
 }


}

}
}