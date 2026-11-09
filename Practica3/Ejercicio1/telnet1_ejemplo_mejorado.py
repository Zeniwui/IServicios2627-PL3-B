# Ejercicio 1 (mejorado): se descarta el mensaje de bienvenida usando read_until()
import getpass
import telnetlib

HOST = "localhost"   # Desde Windows: poner la IP del servidor Ubuntu
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode("utf-8") + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode("utf-8") + b"\n")

# Leer y descartar el mensaje de bienvenida hasta el primer prompt (termina en $)
tn.read_until(b"$")

# Enviar el comando y leer hasta el siguiente prompt: eco del comando + su salida
tn.write(b"ls /home\n")
salida = tn.read_until(b"$")

tn.write(b"exit\n")
tn.read_all()   # Descartar el eco del exit
tn.close()

print(salida.decode("utf-8"))
