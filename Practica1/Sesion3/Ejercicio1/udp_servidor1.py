import socket
import sys

# Comprobar si hay argumento 
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

# Creación del socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print("Servidor escuchando en el puerto: ", puerto)

while True:
    
    datagrama, origen = s.recvfrom(1024)
    print("Se ha recibido un datagrama desde ", origen)
    print("Contiene lo siguiente: ")
    print(datagrama.decode("utf-8"))