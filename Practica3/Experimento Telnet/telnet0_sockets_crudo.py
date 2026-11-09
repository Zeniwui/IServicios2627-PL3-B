# Experimento 2.1.3.1: conexión "en crudo" al puerto 23 y volcado hexadecimal
import socket

HOST = "localhost"


def mostrar_hex(datos):
    """Muestra cada byte de una cadena bytes en hexadecimal."""
    print(" ".join(hex(byte)[2:].upper().zfill(2) for byte in datos))


s = socket.socket()
s.connect((HOST, 23))
respuesta = s.recv(1024)
print(respuesta)
mostrar_hex(respuesta)
s.close()

# Resultado típico: FF FD 18 ...
#   FF = IAC (Interpret As Command)
#   FD = DO
#   18 = 24 -> opción "Terminal Type" (IANA Telnet Options), descrita en el RFC 1091
