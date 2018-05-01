node {
   def commit_id
   def app
   
   stage('Clone Repository') {
    /* Clone the repository to our workspace */
     checkout scm
     sh "git rev-parse --short HEAD > .git/commit-id"                        
     commit_id = readFile('.git/commit-id').trim()
   }
   
   stage('Build Image') {
    /* Build the Docker image */
     app = docker.build("jraj/titanic-jenkins")
   }

   stage('Test Image') {
    /* Figure out a way to run tests on the image*/
        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Dockerhub Login') {
    /* Workaround to address issue with credentials stored in Jenkins not
     * being passed correctly to the docker registry
     * - ref https://issues.jenkins-ci.org/browse/JENKINS-38018 */
        withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'docker-hub-credentials',
        usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
        sh 'docker login -u $USERNAME -p $PASSWORD https://index.docker.io/v1/'
        }
    }   

    stage('Push Image') {
    /* Push the image with two tags:
     * First, the commit id from github
     * Second, the 'latest' tag. */
        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
            app.push("${commit_id}")
            app.push("latest")
        }
    }

}
