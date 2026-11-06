import email.message
import email.utils
import os
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
subject = "Prueba Ejercicio 9 - Correo con fichero adjunto"
data = "Hola, adjunto el logotipo de ATC descargado mediante wget."

# Construir mensaje multipart
mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)

# Leer y adjuntar imagen
ruta_adjunto = os.path.join(os.path.dirname(__file__), "logoatc.gif")
with open(ruta_adjunto, "rb") as f:
    datos_gif = f.read()

mensaje.add_attachment(datos_gif, maintype="image", subtype="gif", filename="atc.gif")

raw_message = mensaje.as_bytes() + b"\r\n.\r\n"

# Conexión TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

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

print("[Cliente]: <Enviando mensaje con adjunto>")
s.sendall(raw_message)
RecvReply(s, b"250")

print("[Cliente]: QUIT")
s.sendall(b"QUIT\r\n")
RecvReply(s, b"221")

s.close()
print("Correo con adjunto enviado con éxito.")
