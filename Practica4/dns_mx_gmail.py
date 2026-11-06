import dns.resolver

# 1. Consultar los registros MX de gmail.com
respuestas_mx = dns.resolver.resolve('gmail.com', 'MX')

lista_servidores = []

for rdata in respuestas_mx:
    nombre_servidor = str(rdata.exchange)
    prioridad = rdata.preference
    
    # 2. Consultar la IP (registro A) para cada servidor de correo
    respuestas_a = dns.resolver.resolve(nombre_servidor, 'A')
    for rdata_a in respuestas_a:
        ip = rdata_a.address
        lista_servidores.append((prioridad, nombre_servidor, ip))

# 3. Ordenar por prioridad (menor número = mayor preferencia)
lista_servidores.sort(key=lambda x: x[0])

# 4. Mostrar por pantalla
for prioridad, nombre_servidor, ip in lista_servidores:
    print(f"{prioridad} {nombre_servidor} {ip}")
