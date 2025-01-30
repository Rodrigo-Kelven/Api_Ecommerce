#!/bin/bash

docker build -t ecommerce-app .
# se quiser que rode em background enquanto faz outras coisas
#docker run -di --name  container_ecommerce-app -p 8000:8000 ecommerce-app

# se quiser que o container suma ao parar a aplicacao
#docker run --rm --name container_ecommerce-app -p 8000:8000 ecommerce-app

docker run --name container_ecommerce-app -p 8000:8000 ecommerce-app
