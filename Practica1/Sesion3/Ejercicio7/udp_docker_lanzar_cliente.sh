#!/bin/bash

echo "Lanzando el cliente interactivo..."

docker run -it --rm --name cliente_hola --network red_practica_udp -v "$PWD":/app -w /app python:3.12 python3 udp_cliente6_broadcast.py