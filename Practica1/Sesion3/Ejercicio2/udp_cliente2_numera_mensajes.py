import socket
import sys

if len(sys.argv) > 1:
    ip = sys.argv[1]
else:
    ip = "localhost"

if len(sys.argv) > 2:
    puerto = int(sys.argv[2])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

numero_mensaje = 1

while True:
    texto = input("Introduce texto a enviar: ")
    
    if texto == "FIN":
        break
    
    # Añadimos el número al principio del datagrama convirtiéndolo a string
    mensaje_completo = str(numero_mensaje) + ": " + texto
    
    s.sendto(mensaje_completo.encode("utf-8"), (ip, puerto))
    
    numero_mensaje = numero_mensaje + 1