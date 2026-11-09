# Ejercicio 17 (opcional): MLSD y extracción solo de los nombres (sin . ni ..)
import ftplib, getpass

HOST = "localhost"
CARPETA = "carpeta"

lista = []


def acumular(linea):
    lista.append(linea)


clave = getpass.getpass("Clave? ")

f = ftplib.FTP(HOST)
f.login("alumno", clave)
f.cwd(CARPETA)

lista = []
resp = f.retrlines("MLSD", acumular)
print("Respuesta del protocolo: ", resp)

print("\nMLSD tal cual:")
for l in lista:
    print(l)

# Formato: "type=file;size=123;modify=...;perm=...; nombre"
print("\nNombres:")
for l in lista:
    if "type=cdir" in l or "type=pdir" in l:
        continue
    nombre = l.split(";")[-1].strip()
    print(nombre)
f.quit()
