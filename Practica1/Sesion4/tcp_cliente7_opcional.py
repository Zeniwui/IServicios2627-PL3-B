from sys import argv

import socket
import struct

if len(argv) < 3:
    host = "localhost"
    puerto = 9999
else:
    host = argv[1]
    puerto = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,puerto))

# Hacemos 3 envíos seguidos sin esperar respuesta
for i in range(3):
    mensaje = b"HOLA"
    longitud = struct.pack(">H",len(mensaje))
    s.sendall(longitud+mensaje) # Enviamos la longitud del mensaje y el propio mensaje concatenado
    print("Mensaje enviado a", (host, puerto))

# Intentamos leer 3 respuestas seguidas
for i in range(3):
    cabecera = s.recv(2)
    if not cabecera:
        print("El servidor cerró la conexión")
        break
    longitud_respuesta = struct.unpack(">H",cabecera)[0]
    respuesta = s.recv(longitud_respuesta)
    print("Respuesta del servidor:")
    print(respuesta.decode("utf-8"))

s.close()    
    