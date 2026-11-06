import socket
import sys

def RecvReply(s, expected_code):
    respuesta = s.recv(1024)
    print(f"[Servidor]: {respuesta.decode('utf-8', errors='replace').strip()}")
    
    codigo = respuesta[:3]
    if codigo != expected_code:
        print(f"Error: se esperaba el código {expected_code.decode()}, pero se recibió {codigo.decode()}", file=sys.stderr)
        s.close()
        sys.exit(1)

# Variables de configuración
server = "relay.uniovi.es"
port = 25
fromaddr = "usuario@uniovi.es"
toaddr = "usuario@uniovi.es"
subject = "Prueba Ejercicio 7 SMTP crudo"
data = "Hola, este es un mensaje enviado mediante SMTP en crudo a traves de un socket TCP."

message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)

# Conexión TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

# 1. Mensaje de bienvenida inicial del servidor (220)
RecvReply(s, b"220")

# 2. Comando HELO
print("[Cliente]: HELO uniovi.es")
s.sendall(b"HELO uniovi.es\r\n")
RecvReply(s, b"250")

# 3. Comando MAIL FROM
print(f"[Cliente]: MAIL FROM:<{fromaddr}>")
s.sendall(f"MAIL FROM:<{fromaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

# 4. Comando RCPT TO
print(f"[Cliente]: RCPT TO:<{toaddr}>")
s.sendall(f"RCPT TO:<{toaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

# 5. Comando DATA
print("[Cliente]: DATA")
s.sendall(b"DATA\r\n")
RecvReply(s, b"354")

# 6. Envío del contenido del mensaje terminado en \r\n.\r\n
print("[Cliente]: <Contenido del mensaje>")
s.sendall(message.encode("utf-8"))
RecvReply(s, b"250")

# 7. Comando QUIT
print("[Cliente]: QUIT")
s.sendall(b"QUIT\r\n")
RecvReply(s, b"221")

s.close()
print("Correo enviado con éxito.")
