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
    fich = sd.makefile(encoding="utf-8",newline="\r\n")
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    #time.sleep(1)
    
    # Bucle de atención al cliente conectado
    while continuar:
        # Primero recibir el mensaje del cliente
        mensaje = fich.readline() 
        if not mensaje:
            print("El cliente ha cerrado la conexión")
            sd.close()
            continuar = False
            break

        mensaje2 = mensaje.strip() # quitar saltos de línea invisibles
        #  Darle la vuelta
        mensaje_invertido = mensaje2[::-1]
        # Finalmente, enviarle la respuesta con un fin de línea añadido
        # Observa la transformación en bytes para enviarlo
        sd.sendall(bytes(mensaje_invertido + "\r\n", "utf8"))


