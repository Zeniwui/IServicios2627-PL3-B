import socket
import sys
import random

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print("Servidor escuchando en el puerto", puerto)

while True:
    datagrama, origen = s.recvfrom(1024)
    
    numero_azar = random.randint(1, 2)
    
    if numero_azar == 1:
        print("Simulando paquete perdido")
    else:
        print("Se ha recibido un datagrama desde", origen)
        print("Contiene lo siguiente:")
        print(datagrama.decode("utf-8"))
        
        # NUEVO
        # Enviamos la confirmación al cliente
        # Usamos .encode("utf-8") porque solo podemos enviar bytes
        s.sendto("OK".encode("utf-8"), origen)