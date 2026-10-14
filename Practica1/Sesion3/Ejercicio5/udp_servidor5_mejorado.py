import socket
import sys
import random

if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

print("Servidor mejorado escuchando en el puerto", puerto)

while True:
    datagrama, origen = s.recvfrom(1024)
    mensaje_decodificado = datagrama.decode("utf-8")
    
    # INICIO OPCIONAL EJERCICIO 5
    # El cliente envía "identificador:texto"
    # Usamos split(":", 1) para partirlo solo por los primeros puntos dobles
    partes = mensaje_decodificado.split(":", 1)
    
    if len(partes) == 2:
        id_mensaje = partes[0]
        texto = partes[1]
    else:
        id_mensaje = "0"
        texto = mensaje_decodificado
    # --- FIN OPCIONAL EJERCICIO 5 ---

    numero_azar = random.randint(1, 2)
    
    if numero_azar == 1:
        print("Simulando paquete perdido")
    else:
        print("Se ha recibido un datagrama desde", origen)
        print("Contiene lo siguiente:", texto)
        
        # INICIO OPCIONAL EJERCICIO 5
        # Enviamos la confirmación con el identificador del emisor
        confirmacion = "OK:" + id_mensaje
        s.sendto(confirmacion.encode("utf-8"), origen)
        # FIN OPCIONAL