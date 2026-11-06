import base64
import getpass
import socket
import ssl
import sys

def RecvReply(s, expected_code):
    buffer = b""
    while True:
        line = b""
        while not line.endswith(b"\r\n"):
            chunk = s.recv(1)
            if not chunk:
                break
            line += chunk
        buffer += line
        print(f"[Servidor]: {line.decode('utf-8', errors='replace').strip()}")
        # En SMTP una línea con '250 ' marca el fin de la respuesta, mientras que '250-' indica que continúa
        if len(line) >= 4 and line[3:4] == b" ":
            break
        elif len(line) >= 3 and len(line) < 4:
            break
    
    codigo = buffer[:3]
    if codigo != expected_code:
        print(f"Error: se esperaba el código {expected_code.decode()}, pero se recibió {codigo.decode()}", file=sys.stderr)
        s.close()
        sys.exit(1)

server = "smtp.gmail.com"
port = 587

# 1. Conexión TCP normal al puerto 587
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
RecvReply(s, b"220")

# 2. Comando EHLO
print("[Cliente]: EHLO localhost")
s.sendall(b"EHLO localhost\r\n")
RecvReply(s, b"250")

# 3. Negociar cifrado TLS con STARTTLS
print("[Cliente]: STARTTLS")
s.sendall(b"STARTTLS\r\n")
RecvReply(s, b"220")

# Envolver el socket con SSL
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# 4. Enviar EHLO sobre el canal seguro
print("[Cliente (SSL)]: EHLO localhost")
sc.sendall(b"EHLO localhost\r\n")
RecvReply(sc, b"250")

# 5. Autenticación con AUTH LOGIN
print("[Cliente (SSL)]: AUTH LOGIN")
sc.sendall(b"AUTH LOGIN\r\n")
RecvReply(sc, b"334")

# Lectura y envío de credenciales
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

sc.sendall(base64.b64encode(username.encode("ascii")) + b"\r\n")
RecvReply(sc, b"334")

sc.sendall(base64.b64encode(password.encode("utf-8")) + b"\r\n")
RecvReply(sc, b"235")

# 6. Datos del mensaje y envío
fromaddr = username
toaddr = input("Destinatario: ")
subject = input("Asunto: ")
data = input("Mensaje: ")

message = f"""To: {toaddr}
From: {fromaddr}
Subject: {subject}\r\n\r\n
{data}
\r\n.\r\n"""

print(f"[Cliente (SSL)]: MAIL FROM:<{fromaddr}>")
sc.sendall(f"MAIL FROM:<{fromaddr}>\r\n".encode("utf-8"))
RecvReply(sc, b"250")

print(f"[Cliente (SSL)]: RCPT TO:<{toaddr}>")
sc.sendall(f"RCPT TO:<{toaddr}>\r\n".encode("utf-8"))
RecvReply(sc, b"250")

print("[Cliente (SSL)]: DATA")
sc.sendall(b"DATA\r\n")
RecvReply(sc, b"354")

print("[Cliente (SSL)]: <Contenido del mensaje>")
sc.sendall(message.encode("utf-8"))
RecvReply(sc, b"250")

print("[Cliente (SSL)]: QUIT")
sc.sendall(b"QUIT\r\n")
RecvReply(sc, b"221")

sc.close()
print("Correo enviado correctamente a través de Gmail.")
