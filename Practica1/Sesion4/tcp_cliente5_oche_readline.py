from sys import argv

import socket

if len(argv) < 3:
    host = "localhost"
    puerto = 9999
else:
    host = argv[1]
    puerto = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,puerto))
fich = s.makefile(encoding="utf-8",newline="\r\n")

# Hacemos 3 envíos seguidos sin esperar respuesta
for i in range(3):
    s.sendall(b"HOLA\r\n")
    print("Mensaje enviado a", (host, puerto))

# Intentamos leer 3 respuestas seguidas
for i in range(3):
    respuesta = fich.readline()
    print("Respuesta del servidor:")
    print(respuesta)

s.close()    
    