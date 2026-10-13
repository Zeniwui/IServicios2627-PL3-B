from sys import argv

import socket
import time

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
    fich = sd.makefile(encoding="utf-8",newline="\n")
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # time.sleep(1)
    
    # Bucle de atención al cliente conectado
    while continuar:
        # Primero recibir el mensaje del cliente
        linea_long = fich.readline() # primero recibimos la longitud del mensaje
        if not linea_long:
            print("Se ha perdido la conexión con el cliente")
            sd.close()
            continuar = False
            break

        longitud = int(linea_long) # pasamos a entero la longitud, eliminando \n
        mensaje = fich.read(longitud) #leemos exactamente del buffer exactamente esos caracteres
        if not mensaje:
            print("El cliente ha cerrado la conexión")
            sd.close()
            continuar = False
            break

        #  Darle la vuelta
        mensaje_invertido = mensaje[::-1]
        longitud_respuesta = "%d\n" % len(bytes(mensaje_invertido, "utf-8")) # Pasamos a ASCII la longitud en bytes
        sd.sendall(bytes(longitud_respuesta + mensaje_invertido, "utf8")) # Enviamos la longitud del mensaje y el propio mensaje invertido concatenado


