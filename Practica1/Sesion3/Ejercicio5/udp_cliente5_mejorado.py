import socket
import sys
import random

if len(sys.argv) > 1:
    ip = sys.argv[1]
else:
    ip = "localhost"

if len(sys.argv) > 2:
    puerto = int(sys.argv[2])
else:
    puerto = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Cliente mejorado listo. Escribe 'FIN' para salir.")

while True:
    texto = input("Introduce texto a enviar: ")
    
    if texto == "FIN":
        break
    
    # --- INICIO OPCIONAL EJERCICIO 5 ---
    # Generamos un número aleatorio para identificar este mensaje concreto
    id_mensaje = str(random.randint(1000, 9999))
    mensaje_completo = id_mensaje + ":" + texto
    # --- FIN OPCIONAL EJERCICIO 5 ---
    
    datos_a_enviar = mensaje_completo.encode("utf-8")
    
    timeout_actual = 0.5
    paquete_entregado = False
    
    while timeout_actual <= 2.0:
        s.sendto(datos_a_enviar, (ip, puerto))
        s.settimeout(timeout_actual)
        
        try:
            datagrama_resp, origen_resp = s.recvfrom(1024)
            respuesta = datagrama_resp.decode("utf-8")
            
            # INICIO OPCIONAL EJERCICIO 5
            # Comprobamos que la confirmación traiga nuestro identificador
            confirmacion_esperada = "OK:" + id_mensaje
            
            if respuesta == confirmacion_esperada:
                print("Confirmación recibida correctamente para el mensaje", id_mensaje)
                paquete_entregado = True
                break
            else:
                print("Aviso: Se recibió un OK extraño, ignorando...")
            # FIN OPCIONAL EJERCICIO 5
                
        except socket.timeout:
            print("Timeout de", timeout_actual, "segundos agotado. Reintentando...")
            timeout_actual = timeout_actual * 2
            
    if paquete_entregado == False:
        print("Puede que el servidor esté caído. Inténtelo más tarde")
        sys.exit(0)