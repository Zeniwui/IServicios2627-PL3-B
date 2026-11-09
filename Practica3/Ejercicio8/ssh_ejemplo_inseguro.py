# Ejercicio 8: acepta ciegamente cualquier clave de host (AutoAddPolicy)
import paramiko
import time
import getpass

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Antes de connect()

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
