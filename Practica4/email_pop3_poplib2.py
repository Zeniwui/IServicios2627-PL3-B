import email
import email.header
import getpass
import poplib

def imprime_resumen_mensaje(msg_bytes):
    # Parsear los bytes recibidos y construir con ellos un objeto EmailMessage
    msg = email.message_from_bytes(msg_bytes)
    
    # Extraemos las cabeceras "From" y "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")
    
    # Si estas cabeceras contienen unicode hay que decodificarlas
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))
    
    # Extraemos el cuerpo
    cuerpo = msg.get_payload()
    
    # Si es multi-part, el payload es una lista de partes
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        if isinstance(parte_1, bytes):
            parte_1 = parte_1.decode("utf-8", errors="replace")
        cuerpo = "---Multipart. Parte 1\n" + str(parte_1)
    elif isinstance(cuerpo, bytes):
        cuerpo = cuerpo.decode("utf-8", errors="replace")
    else:
        cuerpo = str(cuerpo)
        
    # Imprimimos un resumen
    print("From:", remite)
    print("Subject:", asunto)
    print(cuerpo[:500])
    if len(cuerpo) > 500:
        print("...[omitido]")
    print("-" * 80)

server = "pop.gmail.com"

# 1. Leer usuario y contraseña
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

# 2. Conectar por POP3_SSL
pop3_mail = poplib.POP3_SSL(server)

# 3. Autenticación
pop3_mail.user(username)
pop3_mail.pass_(password)

# 4. Obtener el número de mensajes
num_mensajes, _ = pop3_mail.stat()
print(f"\nTotal de mensajes disponibles: {num_mensajes}\n")

# 5. Iterar sobre todos los mensajes y mostrar el resumen decodificado
for i in range(1, num_mensajes + 1):
    print(f"=== Mensaje {i} de {num_mensajes} ===")
    resp, lineas, octetos = pop3_mail.retr(i)
    
    # poplib devuelve una lista de líneas; las unimos con b"\r\n"
    msg_bytes = b"\r\n".join(lineas)
    
    imprime_resumen_mensaje(msg_bytes)

# 6. Cerrar sesión
pop3_mail.quit()
