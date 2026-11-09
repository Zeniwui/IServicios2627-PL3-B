# Ejercicio 11: igual que ssh_ejemplo_seguro.py pero contra otro nodo.
# Nodo usado: contenedor Docker con servidor OpenSSH (usuario uo300819), escuchando en el puerto 2222.
import paramiko
import time
import getpass
import base64

HOST = '127.0.0.1'      # Nodo remoto (contenedor Docker "nodo2")
PUERTO = 2222           # Puerto SSH publicado por el contenedor
USUARIO = 'uo300819'

# Segundo campo de /config/ssh_host_keys/ssh_host_ed25519_key.pub del contenedor
CLAVE_HOST = b'AAAAC3NzaC1lZDI1NTE5AAAAIFCmnG256X/8qj2EazxnYrWnGzvSMIlYBcmM3L32XUjC'

client = paramiko.SSHClient()

key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_HOST))
# Con un puerto distinto de 22, paramiko busca la clave con el nombre "[host]:puerto"
client.get_host_keys().add('[%s]:%d' % (HOST, PUERTO), 'ssh-ed25519', key)

clave = getpass.getpass("Clave de %s en %s:%d: " % (USUARIO, HOST, PUERTO))
client.connect(HOST, port=PUERTO, username=USUARIO, password=clave)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('hostname; whoami; ls -la')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
