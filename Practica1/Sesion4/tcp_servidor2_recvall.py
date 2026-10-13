from sys import argv

import socket
# import time # experimento

def recvall(sock,num_bytes):
    datos = b""

    while len(datos) < num_bytes:
        bytes_restantes = num_bytes - len(datos) # bytes que faltan por leer
        recibido = sock.recv(bytes_restantes) # leemos del socket todos los bytes restantes

        # Si no recibimos nada, el cliente cerró la conexión
        if not recibido:
            return b""

        # Concatenamos lo que vamos recibiendo
        datos += recibido
    return datos

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
    # Bucle de atención al cliente conectado
    # time.sleep(1) # experimento
    while continuar:
        datos = recvall(sd,5)  # Observar que se lee del socket sd, no de s
        datos = datos.decode("ascii")  # Pasar los bytes a caracteres
                # En este ejemplo se asume que el texto recibido es ascii puro
        if datos=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)


