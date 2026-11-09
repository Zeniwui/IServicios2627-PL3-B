# Ejercicio 1: ejemplo de la documentación de telnetlib, modificado para listar /home
# Nota: telnetlib se eliminó en Python 3.13. En 3.13+ instalar: pip install standard-telnetlib
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

tn.write(b"ls /home\n")
tn.write(b"exit\n")

print(tn.read_all().decode("utf-8"))
