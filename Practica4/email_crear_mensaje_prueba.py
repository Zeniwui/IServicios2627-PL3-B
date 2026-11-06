import email.message
import email.policy
import email.utils

mensaje = email.message.EmailMessage()
mensaje['To'] = 'Destinatario Peláez <destinatario@example.com>'
mensaje['From'] = 'Remitente Ñúñez <remitente@example.com>'
mensaje['Subject'] = 'Mensaje con tildes: canción'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Texto con tildes: camión, murciélago, pingüino.")

binario = mensaje.as_bytes()
print(binario.decode("utf-8"))
