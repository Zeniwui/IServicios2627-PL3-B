# Ejercicio 19 (opcional): descarga todos los ficheros (no sub-carpetas) de una carpeta remota
import sys
import ftplib, getpass

HOST = "localhost"
CARPETA = sys.argv[1] if len(sys.argv) > 1 else "carpeta"

lista = []


def acumular(linea):
    lista.append(linea)


clave = getpass.getpass("Clave? ")

f = ftplib.FTP(HOST)
f.login("alumno", clave)
f.cwd(CARPETA)

lista = []
f.retrlines("MLSD", acumular)

for l in lista:
    if "type=file" not in l:          # Salta cdir, pdir y dir (sub-carpetas)
        continue
    nombre = l.split(";")[-1].strip()
    with open(nombre, "wb") as f_local:
        result = f.retrbinary("RETR " + nombre, f_local.write)
    print(nombre, "->", result)

f.quit()
