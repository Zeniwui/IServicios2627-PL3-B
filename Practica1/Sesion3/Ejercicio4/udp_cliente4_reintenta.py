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
    datos_a_enviar = mensaje_completo.encode("utf-8")
    
    timeout_actual = 0.5
    paquete_entregado = False
    
    # Bucle que funciona mientras el timeout no supere 2 segundos
    while timeout_actual <= 2.0:
        s.sendto(datos_a_enviar, (ip, puerto))
        s.settimeout(timeout_actual)
        
        try:
            datagrama_resp, origen_resp = s.recvfrom(1024)
            respuesta = datagrama_resp.decode("utf-8")
            
            if respuesta == "OK":
                print("Confirmación recibida: el mensaje llegó bien.")
                paquete_entregado = True
                break  # Salimos del bucle de reintentos porque hubo éxito
                
        except socket.timeout:
            # Si se pasa el timeuot, avisamos y duplicamos el timeout para el siguiente intento
            print("Timeout de", timeout_actual, "segundos agotado. Reintentando...")
            timeout_actual = timeout_actual * 2
            
    # Si salimos del bucle y el paquete no se entregó, el servidor está caído
    if paquete_entregado == False:
        print("Puede que el servidor esté caído. Inténtelo más tarde")
        sys.exit(0) # Finaliza la ejecución del cliente
        
    # Si se entregó con exito, se aumenta el numero del mensaje
    numero_mensaje = numero_mensaje + 1