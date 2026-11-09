# Ejercicio 2: arranca remotamente udp_servidor3_con_ok.py vía telnet si no está en ejecución
import telnetlib
import time

HOST = "localhost"        # IP del servidor Ubuntu si se lanza desde otra máquina
USUARIO = "uo302320"        # Credenciales incrustadas (mala práctica, pedido por el enunciado)
CLAVE = ""
SERVIDOR = "udp_servidor3_con_ok.py"
CARPETA = "~/IS-2026/Practica3/Ejercicio2"

# 1. Conexión y login
tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(USUARIO.encode("utf-8") + b"\n")
tn.read_until(b"Password: ")
tn.write(CLAVE.encode("utf-8") + b"\n")

# 2. Esperar al prompt
tn.read_until(b"$")

# 3. Listar procesos
tn.write(b"ps -efww\n")   # ww: sin truncar las líneas al ancho de la terminal

# 4. Capturar la salida hasta el siguiente prompt
respuesta = tn.read_until(b"$").decode("utf-8", errors="replace")

# 5./6. Comprobar si el servidor ya corre; si no, lanzarlo
if SERVIDOR in respuesta:
    print("El servidor ya está en ejecución")
else:
    print("El servidor no estaba en ejecución. Lanzándolo...")
    tn.write(("cd %s; nohup python3 %s &\n" % (CARPETA, SERVIDOR)).encode("utf-8"))
    # 7. Dar tiempo a que arranque
    time.sleep(1)

# 8. Cerrar el shell remoto
tn.write(b"exit\n")

# 9. Mostrar lo recibido (depuración)
print(tn.read_all().decode("utf-8", errors="replace"))
tn.close()
