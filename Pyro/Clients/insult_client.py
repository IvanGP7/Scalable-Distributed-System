import Pyro4
import threading
import time
import sys

NUM_REQUESTS = int(sys.argv[1]) if len(sys.argv) > 1 else 10

def worker(server_uri, requests):
    server = Pyro4.Proxy(server_uri)
    for i in range(requests):
        server.add_insult(f"insult_{i}")

# Obtener lista de servidores
name_server = Pyro4.Proxy("PYRONAME:nameserver.node")
servers = name_server.get_workers()
num_servers = len(servers)

if num_servers == 0:
    print("Error: No hay servidores registrados")
    sys.exit(1)

# Calcular peticiones por servidor
requests_per_server = NUM_REQUESTS // num_servers

# Ejecutar prueba
start_time = time.time()

threads = []
for uri in servers:
    t = threading.Thread(target=worker, args=(uri, requests_per_server))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

total_time = time.time() - start_time

# Guardar resultados
result_line = f"InsultClient,{NUM_REQUESTS},{num_servers},{total_time:.4f}\n"
with open("tiempos_clientes.log", "a") as f:
    f.write(result_line)

# Mostrar resultados
print(f"InsultClient - {NUM_REQUESTS} peticiones - {num_servers} servidores")
print(f"Tiempo total: {total_time:.2f} segundos")