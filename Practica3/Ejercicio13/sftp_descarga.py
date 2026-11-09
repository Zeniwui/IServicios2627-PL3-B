# Ejercicio 13: descarga todos los ficheros regulares de una carpeta remota vía SFTP
# Uso: python3 sftp_descarga.py <carpeta_remota> [carpeta_local]
import os
import sys
import paramiko
import getpass
import base64
from stat import S_ISDIR

HOST = 'localhost'
USUARIO = 'alumno'
# Segundo campo de /etc/ssh/ssh_host_ed25519_key.pub del servidor
CLAVE_HOST = b'AAAAC3NzaC1lZDI1NTE5AAAA_PEGAR_AQUI_LA_CLAVE_PUBLICA'

if len(sys.argv) < 2:
    print("Uso: %s <carpeta_remota> [carpeta_local]" % sys.argv[0])
    sys.exit(1)
carpeta_remota = sys.argv[1]
carpeta_local = sys.argv[2] if len(sys.argv) > 2 else "."
os.makedirs(carpeta_local, exist_ok=True)

c = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_HOST))
c.get_host_keys().add(HOST, 'ssh-ed25519', key)

clave = getpass.getpass("Clave de %s: " % USUARIO)
c.connect(HOST, username=USUARIO, password=clave)

sftp = c.open_sftp()
sftp.chdir(carpeta_remota)

descargados = 0
for nombre in sftp.listdir():
    if S_ISDIR(sftp.stat(nombre).st_mode):
        print("Omitida carpeta:", nombre)
        continue
    sftp.get(nombre, os.path.join(carpeta_local, nombre))
    print("Descargado:", nombre)
    descargados += 1

print("Total ficheros descargados:", descargados)
sftp.close()
c.close()
