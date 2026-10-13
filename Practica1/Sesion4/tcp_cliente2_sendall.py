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

contador = 0
while contador < 5:
    s.sendall(b"ABCD")
    print("Mensaje enviado a ",(host,puerto))
    contador += 1


s.sendall(b"FINAL")
print("Mensaje de finalización enviado. Cerrando socket")
s.close()    
    