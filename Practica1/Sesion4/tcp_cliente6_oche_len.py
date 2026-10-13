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
fich = s.makefile(encoding="utf-8",newline="\n")

# Hacemos 3 envíos seguidos sin esperar respuesta

for i in range(3):
    mensaje = "HOLA"
    longitud = "%d\n" % len(bytes(mensaje, "utf-8")) # Pasamos a ASCII la longitud en bytes
    s.sendall(bytes(longitud + mensaje, "utf8")) # Enviamos la longitud del mensaje y el propio mensaje concatenado
    print("Mensaje enviado a", (host, puerto))

# Intentamos leer 3 respuestas seguidas
for i in range(3):
    linea_long = fich.readline()
    if not linea_long:
        print("El servidor cerró la conexión")
        break
    longitud_respuesta = int(linea_long) # pasamos a entero, para eliminar \n
    respuesta = fich.read(longitud_respuesta) # Leemos del buffer exactamente ese número de caracteres
    print("Respuesta del servidor:")
    print(respuesta)

s.close()    
    