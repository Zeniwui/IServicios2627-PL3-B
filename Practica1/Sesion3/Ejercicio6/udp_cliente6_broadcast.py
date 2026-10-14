import socket
import sys


if len(sys.argv) > 1:
    ip_broadcast = sys.argv[1]
else:
    ip_broadcast = "<broadcast>"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Enviando mensaje BUSCANDO HOLA a:", ip_broadcast)
s.sendto("BUSCANDO HOLA".encode("utf-8"), (ip_broadcast, 12345))


s.settimeout(2.0)
primera_ip = None

while True:
    try:
        datagrama, origen = s.recvfrom(65535)
        mensaje = datagrama.decode("utf-8")
        ip_servidor = origen[0]
        
        if mensaje == "IMPLEMENTO HOLA":
            print("Ha respondido un servidor desde la IP:", ip_servidor)
            
            if primera_ip == None:
                primera_ip = ip_servidor
                
    except socket.timeout:
        print("Fin del tiempo de búsqueda.")
        break

if primera_ip != None:
    print("Vamos a enviarle el HOLA al servidor:", primera_ip)
    
    s.sendto("HOLA".encode("utf-8"), (primera_ip, 12345))
    
    s.settimeout(2.0)
    try:
        datagrama_final, origen_final = s.recvfrom(65535)
        print("Respuesta final del servidor:", datagrama_final.decode("utf-8"))
    except socket.timeout:
        print("El servidor no contestó a nuestro HOLA.")
else:
    print("No se encontró ningún servidor HOLA en la red.")