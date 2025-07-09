//Jenkinsfile

// Define el agente donde se ejecutará el pipeline.
// 'any' significa que puede ejecutarse en cualquier agente disponible.
// Podríamos especificar un agente con Docker si tuviéramos uno configurado.
pipeline{    
    agent any

// Define las herramientas que Jenkins debe cargar para este pipeline.
    tools{
        git 'Default'
      }

    // Opciones globales para el pipeline
    options {
        // Borra el workspace antes de cada build para asegurar un entorno limpio
        skipDefaultCheckout() // Saltar el checkout por defecto para hacer uno personalizado
        timeout(time: 15, unit: 'MINUTES') // Tiempo máximo para el pipeline
    }

    // Definición de las etapas del pipeline
    stages {
        stage('Checkout Code') {
            steps {
                // Clonar el repositorio desde GitHub usando la credencial SSH que se configuraron 
                // 'jenkins-ssh-key' es el ID de la credencial en Jenkins.
                // El URL es el que corresponde al SSH del repo 
                git url: 'git@github.com:franconl/fastapi-todo-cicd-project.git',
                    credentialsId: 'jenkins-ssh-key',
                    branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Se construye la imagen Docker.
                    // 'docker build -t fastapi-todo-app .' construirá la imagen
                    // y la etiquetará con 'fastapi-todo-app'.
                    sh 'docker build -t fastapi-todo-app .'
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    // Ejecuta los tests unitarios dentro de un nuevo contenedor basado en la imagen que acabamos de construir.
                    // '--rm' asegura que el contenedor sea eliminado después de la ejecución.
                    // 'pytest tests/test_main.py' es el comando para ejecutar tus tests.
                    sh 'docker run --rm fastapi-todo-app pytest tests/test_main.py'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Primero, detiene y elimina cualquier contenedor existente con el mismo nombre.
                    // Esto evita conflictos de puertos si ya hay una instancia corriendo.
                    // Se usa '|| true' para que el comando no falle si el contenedor no existe.
                    sh 'docker stop fastapi-todo-container || true'
                    sh 'docker rm fastapi-todo-container || true'

                    // Despliega la nueva versión de la aplicación.
                    // '-d' para ejecutar en segundo plano.
                    // '-p 80:8000' para mapear puertos.
                    // '--name' para darle un nombre al contenedor.
                    sh 'docker run -d --name fastapi-todo-container -p 80:8000 fastapi-todo-app'
                }
            }
        }
    }
  
    // Define las acciones a realizar después de que el pipeline termina (éxito o fallo)
    post {
        always {
            //notificar.
            echo 'Pipeline finished.'
        }
        success {
            // Solo se ejecuta si todas las etapas fueron exitosas.
            echo 'Pipeline executed successfully! Application deployed.'
        }
        failure {
            // Solo se ejecuta si alguna etapa falló.
            echo 'Pipeline failed. Check logs for details.'
        }
    }


  }
