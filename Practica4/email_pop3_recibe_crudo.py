import email
import getpass
import socket
import ssl
import sys

def RecvReply(sc):
    respuesta = sc.recv(1024)
    print(f"[Servidor]: {respuesta.decode('utf-8', errors='replace').strip()}")
    
    if not respuesta.startswith(b"+OK"):
        print(f"Error: la respuesta no comienza por +OK", file=sys.stderr)
        sc.close()
        sys.exit(1)
    return respuesta

server = "pop.gmail.com"
port = 995

# 3. Leer usuario y contraseña por teclado
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

# 4. Crear la conexión de socket y canal seguro
s = socket.socket()
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# Leer bienvenida inicial del servidor POP3 (+OK)
RecvReply(sc)

# 5. Enviar USER y PASS
sc.sendall(f"USER {username}\r\n".encode("utf-8"))
RecvReply(sc)

sc.sendall(f"PASS {password}\r\n".encode("utf-8"))
RecvReply(sc)

# 6. Enviar STAT para consultar cuántos correos hay disponibles
sc.sendall(b"STAT\r\n")
resp_stat = RecvReply(sc)
# Formato de respuesta: +OK <num_mensajes> <tamaño_total>
partes = resp_stat.decode("utf-8", errors="replace").split()
num_mensajes = int(partes[1])
print(f"Número de mensajes disponibles: {num_mensajes}")

if num_mensajes > 0:
    # 7. Leer el contenido del primer correo (RETR 1)
    sc.sendall(b"RETR 1\r\n")
    
    correo_bytes = b""
    while not correo_bytes.endswith(b"\r\n.\r\n"):
        chunk = sc.recv(4096)
        if not chunk:
            break
        correo_bytes += chunk
    
    # Quitar la primera línea (+OK ...) y el punto final (\r\n.\r\n)
    lineas = correo_bytes.split(b"\r\n", 1)
    cuerpo_correo = lineas[1] if len(lineas) > 1 else correo_bytes
    if cuerpo_correo.endswith(b"\r\n.\r\n"):
        cuerpo_correo = cuerpo_correo[:-3]
    
    # 8. Extraer campos Subject y From de las cabeceras
    msg = email.message_from_bytes(cuerpo_correo)
    print("\n--- Cabeceras del mensaje 1 ---")
    print(f"From: {msg.get('From', '<desconocido>')}")
    print(f"Subject: {msg.get('Subject', '<sin asunto>')}")
else:
    print("No hay mensajes disponibles en el buzón POP3.")

# Cerrar sesión con QUIT
sc.sendall(b"QUIT\r\n")
RecvReply(sc)
sc.close()
