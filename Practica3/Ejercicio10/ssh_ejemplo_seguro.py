# Ejercicio 10: política por defecto (RejectPolicy) + registro de la clave pública conocida del servidor
import paramiko
import time
import getpass
import base64

# Segundo campo de /etc/ssh/ssh_host_ed25519_key.pub del servidor
#   $ cat /etc/ssh/ssh_host_ed25519_key.pub
#   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA......  root@maquina
# Copiar aquí SOLO la parte "AAAAC3Nza..." (sin "ssh-ed25519" ni "root@...")
CLAVE_HOST = b'AAAAC3NzaC1lZDI1NTE5AAAAIA3RAhsUfcsrYWxkEYu9Gs7M1YyiW32AS0VJ8WDIvp7v'

client = paramiko.SSHClient()

key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_HOST))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)  # Antes de connect()

clave = getpass.getpass("Clave de uo302320: ")
client.connect('localhost', username='uo302320', password=clave)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
