import socket

HOST = "en.wikipedia.org"
SERVICE = "www"

# 1. Obtener información de conexión mediante getaddrinfo()
info = socket.getaddrinfo(HOST, SERVICE, socket.AF_UNSPEC, socket.SOCK_STREAM)

# 2. Conexión por IPv4
print("=== Intento de conexión por IPv4 ===")
ipv4_entries = [entry for entry in info if entry[0] == socket.AF_INET]

if ipv4_entries:
    family, socktype, proto, canonname, sockaddr = ipv4_entries[0]
    print(f"Conectando a {sockaddr}...")
    
    s_ipv4 = socket.socket(family, socktype, proto)
    s_ipv4.connect(sockaddr)
    
    # 3. Enviar petición HTTP para solicitar la raíz (/)
    peticion = f"GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
    s_ipv4.sendall(peticion.encode("utf-8"))
    
    # 4. Recibir y mostrar la respuesta del servidor
    respuesta = b""
    while True:
        datos = s_ipv4.recv(4096)
        if not datos:
            break
        respuesta += datos
    
    s_ipv4.close()
    print("Respuesta recibida:")
    print(respuesta.decode("utf-8", errors="replace")[:1000])
    print("...\n")
else:
    print("No se encontraron entradas IPv4.")

# 5. Intento de conexión por IPv6
print("=== Intento de conexión por IPv6 ===")
try:
    info_v6 = socket.getaddrinfo(HOST, SERVICE, socket.AF_INET6, socket.SOCK_STREAM)
    family, socktype, proto, canonname, sockaddr = info_v6[0]
    print(f"Conectando por IPv6 a {sockaddr}...")
    s_ipv6 = socket.socket(family, socktype, proto)
    s_ipv6.connect(sockaddr)
    print("Conexión IPv6 establecida con éxito.")
    s_ipv6.close()
except Exception as e:
    print(f"Error al conectar por IPv6 (esperado, la red no lo soporta): {e}")
