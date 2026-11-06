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

# 1. Leer usuario y contraseña por teclado
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

# 2. Conexión de socket y canal seguro SSL
s = socket.socket()
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# Bienvenida inicial
RecvReply(sc)

# 3. Autenticación USER y PASS
sc.sendall(f"USER {username}\r\n".encode("utf-8"))
RecvReply(sc)

sc.sendall(f"PASS {password}\r\n".encode("utf-8"))
RecvReply(sc)

# 4. Consultar número de mensajes con STAT
sc.sendall(b"STAT\r\n")
resp_stat = RecvReply(sc)
partes = resp_stat.decode("utf-8", errors="replace").split()
num_mensajes = int(partes[1])
print(f"\nTotal de mensajes disponibles: {num_mensajes}\n")

# 5. Iterar sobre todos los mensajes disponibles y mostrar From y Subject
for i in range(1, num_mensajes + 1):
    sc.sendall(f"RETR {i}\r\n".encode("utf-8"))
    
    correo_bytes = b""
    while not correo_bytes.endswith(b"\r\n.\r\n"):
        chunk = sc.recv(4096)
        if not chunk:
            break
        correo_bytes += chunk
    
    # Separar la primera línea (+OK ...) y descartar el .\r\n final
    lineas = correo_bytes.split(b"\r\n", 1)
    cuerpo_correo = lineas[1] if len(lineas) > 1 else correo_bytes
    if cuerpo_correo.endswith(b"\r\n.\r\n"):
        cuerpo_correo = cuerpo_correo[:-3]
    
    # Parsear cabeceras con el módulo email
    msg = email.message_from_bytes(cuerpo_correo)
    print(f"--- Mensaje {i} ---")
    print(f"From: {msg.get('From', '<desconocido>')}")
    print(f"Subject: {msg.get('Subject', '<sin asunto>')}")
    print("-" * 40)

# 6. Salir
sc.sendall(b"QUIT\r\n")
RecvReply(sc)
sc.close()
