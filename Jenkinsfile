pipeline{
    agent any

    environment{
        VEVN_DIR = 'venv'
    }

    stages{
        stage('Cloning GitHub repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins ......'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/antongduy2307/MLOps-House-Pricing.git']])
                }
            }
        }

        stage('Setting up Python Virtual Environment and installing dependencies'){
            steps{
                script{
                    echo 'Setting up Python Virtual Environment and installing dependencies ......'
                    sh '''
                    python -m venv ${VENV_DIR}
                    .${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}