# Ejercicio 9: WarningPolicy -> acepta la clave pero avisa.
# Los bytes del aviso son el fingerprint MD5 (en hex) de la clave pública del servidor.
# Verificación en el servidor:  ssh-keygen -l -E md5 -f /etc/ssh/ssh_host_ed25519_key.pub
import paramiko
import time
import getpass

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())  # Antes de connect()

clave = getpass.getpass("Clave de alumno: ")
client.connect('localhost', username='uo302320', password=clave)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
