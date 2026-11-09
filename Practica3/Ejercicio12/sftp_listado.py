# Ejercicio 12: listado de la carpeta home del usuario remoto vía SFTP
import paramiko
import getpass
import base64

HOST = 'localhost'
USUARIO = 'alumno'
# Segundo campo de /etc/ssh/ssh_host_ed25519_key.pub del servidor
CLAVE_HOST = b'AAAAC3NzaC1lZDI1NTE5AAAA_PEGAR_AQUI_LA_CLAVE_PUBLICA'

c = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_HOST))
c.get_host_keys().add(HOST, 'ssh-ed25519', key)

clave = getpass.getpass("Clave de %s: " % USUARIO)
c.connect(HOST, username=USUARIO, password=clave)

sftp = c.open_sftp()          # La carpeta remota por defecto es el home del usuario
for nombre in sftp.listdir():
    print(nombre)

sftp.close()
c.close()
