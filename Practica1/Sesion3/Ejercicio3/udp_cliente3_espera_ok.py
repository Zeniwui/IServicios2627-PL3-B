import socket
import sys

if len(sys.argv) > 1:
    ip = sys.argv[1]
else:
    ip = "localhost"

if len(sys.argv) > 2:
    puerto = int(sys.argv[2])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

numero_mensaje = 1

while True:
    texto = input("Introduce texto a enviar: ")
    
    if texto == "FIN":
        break
    
    mensaje_completo = str(numero_mensaje) + ": " + texto
    s.sendto(mensaje_completo.encode("utf-8"), (ip, puerto))
    
    # NUEVO 
    # Configuramos un tiempo de espera máximo
    s.settimeout(2.0)
    
    try:
        # Intentamos recibir la confirmación
        datagrama_resp, origen_resp = s.recvfrom(1024)
        respuesta = datagrama_resp.decode("utf-8")
        
        if respuesta == "OK":
            print("Confirmación recibida: el mensaje llegó bien.")
            
    except socket.timeout:
        # Si pasan los 2 segundos y no llega nada, se ejecuta esto
        print("ERROR. El datagrama de confirmación no llega")
        
    numero_mensaje = numero_mensaje + 1