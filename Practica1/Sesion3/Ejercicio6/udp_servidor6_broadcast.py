import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

s.bind(("", 12345))

print("Servidor HOLA esperando mensajes en el puerto 12345...")

while True:
    datagrama, origen = s.recvfrom(65535)
    mensaje = datagrama.decode("utf-8")
    
    ip_cliente = origen[0]
    
    if mensaje == "BUSCANDO HOLA":
        print("Petición de búsqueda recibida desde:", ip_cliente)
        s.sendto("IMPLEMENTO HOLA".encode("utf-8"), origen)
        
    elif mensaje == "HOLA":
        print("Petición de servicio recibida desde:", ip_cliente)
        respuesta = "HOLA: " + ip_cliente
        s.sendto(respuesta.encode("utf-8"), origen)