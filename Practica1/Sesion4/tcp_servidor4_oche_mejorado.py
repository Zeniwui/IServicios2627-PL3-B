from sys import argv

import socket
# import time

def recibe_mensaje(sd):
    buffer = []
    while True:
        # Leemos byte a byte
        byte = sd.recv(1)

        if not byte: # cierre de conexión
            return b""
        
        buffer.append(byte)
        # Si es fin de mensaje, cortamos 
        if byte == b"\n":
            break

    return b"".join(buffer)

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
        mensaje = recibe_mensaje(sd)  
        if not mensaje:
            print("El cliente ha cerrado la conexión")
            sd.close()
            continuar = False
            break
        
        mensaje = str(mensaje, "utf8") # Convertir los bytes a caracteres
        
        # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
        linea = mensaje[:-2]  # slice desde el principio hasta el final -2

        # Tercero, darle la vuelta
        linea = linea[::-1]

        # Finalmente, enviarle la respuesta con un fin de línea añadido
        # Observa la transformación en bytes para enviarlo
        sd.sendall(bytes(linea+"\r\n", "utf8"))


