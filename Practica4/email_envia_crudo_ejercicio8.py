import email.message
import email.utils
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
subject = "Prueba Ejercicio 8 - EmailMessage con tildes: canción"
data = "Hola, este es un mensaje con caracteres no ASCII: camión, pingüino, año."

# Construcción del mensaje con la biblioteca email
mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)

# Obtener bytes del mensaje y añadir el punto final requerido por SMTP en crudo
raw_message = mensaje.as_bytes() + b"\r\n.\r\n"

# Conexión TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

# Protocolo SMTP
RecvReply(s, b"220")

print("[Cliente]: HELO uniovi.es")
s.sendall(b"HELO uniovi.es\r\n")
RecvReply(s, b"250")

print(f"[Cliente]: MAIL FROM:<{fromaddr}>")
s.sendall(f"MAIL FROM:<{fromaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

print(f"[Cliente]: RCPT TO:<{toaddr}>")
s.sendall(f"RCPT TO:<{toaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

print("[Cliente]: DATA")
s.sendall(b"DATA\r\n")
RecvReply(s, b"354")

print("[Cliente]: <Enviando mensaje generado por EmailMessage>")
s.sendall(raw_message)
RecvReply(s, b"250")

print("[Cliente]: QUIT")
s.sendall(b"QUIT\r\n")
RecvReply(s, b"221")

s.close()
print("Correo enviado con éxito.")
