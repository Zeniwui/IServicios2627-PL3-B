# Ejercicio 18 (opcional): descarga de prueba.txt como prueba-copia.txt
import ftplib, getpass

HOST = "localhost"
CARPETA = "carpeta"     # Carpeta remota donde está prueba.txt

clave = getpass.getpass("Clave? ")

f = ftplib.FTP(HOST)
f.login("alumno", clave)
f.cwd(CARPETA)

f_local = open("prueba-copia.txt", "wb")    # Creamos el fichero local
                                            # importante abrirlo en modo binario "b"
result = f.retrbinary("RETR prueba.txt",    # Enviar petición de fichero
                      f_local.write)        # Función a ejecutar por cada bloque recibido
f_local.close()
print(result)
f.quit()
