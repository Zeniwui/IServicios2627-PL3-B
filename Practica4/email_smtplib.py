import email.message
import email.utils
import getpass
import smtplib

server = "smtp.gmail.com"
port = 587

# 1. Instanciar objeto SMTP y activar depuración del protocolo
s = smtplib.SMTP(server, port)
s.set_debuglevel(1)

# 2. Negociar canal seguro (STARTTLS)
s.starttls()

# 3. Pedir credenciales por teclado e iniciar sesión
username = input("Usuario (Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")
s.login(username, password)

# 4. Datos del mensaje
fromaddr = username
toaddr = input("Destinatario: ")
subject = input("Asunto: ")
data = input("Mensaje: ")

# Construir el mensaje con email.message
mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)

# 5. Enviar mensaje usando .as_bytes() y cerrar conexión
s.sendmail(fromaddr, [toaddr], mensaje.as_bytes())
s.quit()

print("Correo enviado con éxito mediante smtplib.")
