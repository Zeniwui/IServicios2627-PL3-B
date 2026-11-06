import dns.resolver

respuestas = dns.resolver.resolve('apple.com', 'A')
  
for rdata in respuestas: 
  print(rdata.address) 