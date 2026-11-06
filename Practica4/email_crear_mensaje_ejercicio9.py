import email.message
import email.utils
import mimetypes
import os

mensaje = email.message.EmailMessage()
mensaje['To'] = 'Destinatario <destinatario@example.com>'
mensaje['From'] = 'Remitente <remitente@example.com>'
mensaje['Subject'] = 'Mensaje con adjunto (Ejercicio 9)'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Adjunto se incluye el logotipo de ATC.")

ruta_adjunto = os.path.join(os.path.dirname(__file__), "logoatc.gif")
with open(ruta_adjunto, "rb") as f:
    datos_adjunto = f.read()

mensaje.add_attachment(datos_adjunto, maintype="image", subtype="gif", filename="atc.gif")

binario = mensaje.as_bytes()
print(binario.decode("utf-8", errors="replace"))
