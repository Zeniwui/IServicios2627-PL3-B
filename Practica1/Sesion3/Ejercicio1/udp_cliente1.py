import socket
import sys

# Obtener IP y puerto de los argumentos (o usar localhost y 9999 por defecto)
ip = sys.argv[1] if len(sys.argv) > 1 else "localhost"
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Listo para enviar a" + str(ip) + " : " + str(puerto) + " . Escribe 'FIN' para salir.")

while True:
    texto = input("Introduce texto a enviar: ")
    if texto == "FIN":
        break
    
    # Enviar los datos convertidos a bytes
    s.sendto(texto.encode("utf-8"), (ip, puerto))