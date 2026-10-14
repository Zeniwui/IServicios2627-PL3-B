#!/bin/bash

echo "Creando la red virtual de Docker..."

docker network create red_practica_udp || true

echo "Lanzando 3 servidores en segundo plano..."

# Lanzamos el Servidor 1 (-d para segundo plano, conectándolo a la red y montando la carpeta actual)
docker run -d --rm --name servidor_hola_1 --network red_practica_udp -v "$PWD":/app -w /app python:3.12 python3 udp_servidor6_broadcast.py

# Lanzamos el Servidor 2
docker run -d --rm --name servidor_hola_2 --network red_practica_udp -v "$PWD":/app -w /app python:3.12 python3 udp_servidor6_broadcast.py

# Lanzamos el Servidor 3
docker run -d --rm --name servidor_hola_3 --network red_practica_udp -v "$PWD":/app -w /app python:3.12 python3 udp_servidor6_broadcast.py

echo "¡Servidores lanzados! Puedes comprobar que están corriendo ejecutando 'docker ps'."