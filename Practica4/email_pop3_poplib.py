import getpass
import poplib

server = "pop.gmail.com"

# 1. Leer usuario y contraseña
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

# 2. Instanciar el objeto POP3_SSL y activar nivel de depuración
pop3_mail = poplib.POP3_SSL(server)
pop3_mail.set_debuglevel(2)

# 3. Autenticación con user() y pass_()
pop3_mail.user(username)
pop3_mail.pass_(password)

# 4. Obtener información de la bandeja
num_mensajes, total_tamano = pop3_mail.stat()
print(f"\nMensajes disponibles: {num_mensajes}")

# 5. Descargar el primer mensaje con retr() y mostrarlo tal como poplib lo devuelve
if num_mensajes > 0:
    # retr() retorna tupla: (respuesta_servidor, lineas_mensaje, tamano_bytes)
    resp, lineas, octetos = pop3_mail.retr(1)
    
    print("\n=== RESPUESTA DEL SERVIDOR ===")
    print(resp)
    
    print(f"\n=== TAMAÑO (OCTETOS): {octetos} ===")
    
    print("\n=== CONTENIDO (TAL COMO POPLIB LO DEVUELVE) ===")
    print(f"Tipo devuelto: {type(lineas)}, con {len(lineas)} líneas.")
    print("Contenido:")
    for linea in lineas:
        print(linea.decode("utf-8", errors="replace"))
else:
    print("No hay mensajes disponibles en la cuenta.")

# 6. Cerrar sesión
pop3_mail.quit()
