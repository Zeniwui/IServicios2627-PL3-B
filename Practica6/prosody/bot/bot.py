from slixmpp import ClientXMPP
import logging          # Para el log de depuración
import getpass          # Para pedir la contraseña de forma segura
import os               # Para obtener variables de entorno (contraseña, para docker)
import ssl              # Para manejar certificados SSL

class MiBot(ClientXMPP):
    def __init__(self, jid, clave):
        # Llamamos al constructor de la clase base con el jid y la clave
        super().__init__(jid, clave)
        # Registrar los eventos y sus manejadores
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)

        # Eventos de la extensión chatstates (XEP-0085)
        self.add_event_handler("chatstate_active", self.callback_activo)
        self.add_event_handler("chatstate_composing", self.callback_escribiendo)
        self.add_event_handler("chatstate_paused", self.callback_pausa)
        self.add_event_handler("chatstate_inactive", self.callback_inactivo)

    # Implementación de los callbacks (todos son tipo async)
    async def callback_para_session_start(self, event):
        print("Sesión iniciada!")
        # Anunciamos que el bot está online
        self.send_presence()
        
        # get_roster() es una corutina por lo que hay que usar 'await'
        await self.get_roster()
        print("Roster recibido.")

    async def callback_para_message(self, event):
        # Solo respondemos a los mensajes de chat que tengan texto
        if event["type"] != "chat" or not event["body"]:
            return

        origen = event["from"]
        cuerpo = event["body"]
        print(f"Recibido un mensaje de tipo {event['type']} de {origen}")
        print(f"Que dice: {cuerpo}")

        if cuerpo.startswith("="):
            # Modo calculadora: evaluamos lo que va detrás del '='
            expresion = cuerpo[1:]
            try:
                # Sin acceso a funciones ni variables del programa
                resultado = eval(expresion, {"__builtins__": {}}, {})
                respuesta = str(resultado)
            except Exception as e:
                respuesta = f"Error en la expresión: {e}"
        else:
            # Modo eco
            respuesta = "¿%s?" % cuerpo

        msg = self.Message()
        msg["to"] = origen
        msg["type"] = "chat"
        msg["body"] = respuesta
        msg["chat_state"] = "active"
        msg.send()
        print(f"Respondido: {respuesta}")

    # Callbacks para los estados del chat
    async def callback_activo(self, event):
        print(f"{event['from'].bare} está activo")

    async def callback_escribiendo(self, event):
        print(f"{event['from'].bare} está escribiendo...")

    async def callback_pausa(self, event):
        print(f"{event['from'].bare} ha parado de escribir")

    async def callback_inactivo(self, event):
        print(f"{event['from'].bare} está inactivo")

# Programa principal
if __name__ == "__main__":
    # Depuración
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')

    # Datos de conexión
    jid = "bot@ingserv3b"
    # En el host se usa localhost; en Docker se indica el nombre del contenedor de prosody
    ip = os.environ.get("SERVIDOR_XMPP", "localhost")
    port = 5222

    # La contraseña nunca va en el código: variable de entorno o teclado
    clave = os.environ.get("CLAVEBOT")
    if clave is None:
        clave = getpass.getpass("Contraseña del bot: ")

    # Certificado autofirmado del servidor (generado con prosodyctl)
    # Ruta del certificado del servidor (en Docker se copia dentro de la imagen)
    cert_file = os.environ.get("CERT_FILE", "../etc/prosody/certs/ingserv3b.crt")
    ssl_context = ssl.create_default_context()

    if os.path.exists(cert_file):
        print(f"Cargando certificado de confianza desde: {cert_file}")
        ssl_context.load_verify_locations(cert_file)
        # El certificado es para 'ingserv3b', pero conectamos a 'localhost'
        print("Desactivando la comprobación de hostname.")
        ssl_context.check_hostname = False
    else:
        print(f"ADVERTENCIA: No se encontró '{cert_file}'. Desactivando TODA la validación de certificado.")
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    # Instanciar el bot y asignarle el contexto SSL
    client = MiBot(jid, clave)
    client.ssl_context = ssl_context

    # Completar con registro del plugin
    client.register_plugin("xep_0085")      # chatstates
    
    # Conectar con el servidor e iniciar el bucle de eventos
    client.connect((ip, port))
    client.process(forever=True)