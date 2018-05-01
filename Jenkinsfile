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

   stage('Test image') {
    /* Figure out a way to run tests on the image*/
        app.inside {
            sh 'echo "Tests passed"'
        }
    }

stage('Push image') {
        /* Push the image with two tags:
         * First, the commit id from github
         * Second, the 'latest' tag. */
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${commit_id}")
            app.push("latest")
        }
    }


}