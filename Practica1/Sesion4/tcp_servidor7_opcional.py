from sys import argv

import socket
import time
import struct

if len(argv) < 2:
    puerto = 9999
else:
    puerto = int(argv[1])

print("Servidor TCP escuchando en el puerto", puerto)

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

# Asignarle puerto
s.bind(("", puerto))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # time.sleep(1)
    
    # Bucle de atención al cliente conectado
    while continuar:
        # Primero recibir el mensaje del cliente
        cabecera = sd.recv(2) # leemos la longitud, por lo que esperamos solo 2 bytes
        if not cabecera:
            print("El cliente ha cerrado la conexión")
            sd.close()
            continuar = False
            break
        longitud = struct.unpack(">H",cabecera)[0] # obtenemos la longitud
        mensaje = sd.recv(longitud)
        if not mensaje:
            print("El cliente ha cerrado la conexión")
            sd.close()
            continuar = False
            break
        mensaje = mensaje.decode("utf-8")
        #  Darle la vuelta
        mensaje_invertido = mensaje[::-1]
        mensaje_invertido_bytes = mensaje_invertido.encode("utf-8")

        longitud_respuesta = struct.pack(">H",len(mensaje_invertido_bytes))
        sd.sendall(longitud_respuesta + mensaje_invertido_bytes) 

