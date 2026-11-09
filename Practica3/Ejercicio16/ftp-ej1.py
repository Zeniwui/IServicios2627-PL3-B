# Ejercicio 16 (opcional): LIST de una carpeta remota vía FTP
# Comenzamos por definir el callback, que es una función
# que sera llamada por cada linea recibida del servidor
# Este callback se limita a acumular las lineas en una
# variable global llamada lista
import ftplib, getpass

HOST = "localhost"     # Cambiar por la IP del compañero para la 2ª parte
CARPETA = "carpeta"

lista = []


def acumular(linea):
    lista.append(linea)


clave = getpass.getpass("Clave? ")

f = ftplib.FTP(HOST)        # Conecta al servidor
f.login("alumno", clave)    # Envía comandos USER y PASS
f.cwd(CARPETA)              # Envía comando CWD

# Borramos la lista donde recibiremos la respuesta
lista = []
# Enviamos comando LIST e indicamos el callback para tratar la respuesta
resp = f.retrlines("LIST", acumular)

# Mostramos los resultados
print("Respuesta del protocolo: ", resp)
print("Contenidos de la carpeta remota:")
for l in lista:
    print(l)
f.quit()
