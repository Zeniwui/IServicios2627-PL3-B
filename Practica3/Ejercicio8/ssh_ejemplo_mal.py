# Versión que NO funciona: la clave del host es desconocida (RejectPolicy por defecto)
# Excepción: paramiko.ssh_exception.SSHException: Server 'localhost' not found in known_hosts
import paramiko
import time
client = paramiko.SSHClient()
client.connect('localhost', username='uo302320', password='clave-mal')
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
