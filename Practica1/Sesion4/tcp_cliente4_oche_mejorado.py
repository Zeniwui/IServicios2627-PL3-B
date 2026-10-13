from sys import argv

import socket

def recibe_mensaje(s):
    buffer = []
    while True:
        # Leemos byte a byte
        byte = s.recv(1)

        if not byte: # cierre de conexión
            return b""
        
        buffer.append(byte)
        # Si es fin de mensaje, cortamos 
        if byte == b"\n":
            break

    return b"".join(buffer)

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
    s.sendall(b"HOLA\r\n")
    print("Mensaje enviado a", (host, puerto))

# Intentamos leer 3 respuestas seguidas
for i in range(3):
    respuesta = recibe_mensaje(s)
    print("Respuesta del servidor:")
    print(repr(respuesta.decode("utf-8")))

s.close()    
    