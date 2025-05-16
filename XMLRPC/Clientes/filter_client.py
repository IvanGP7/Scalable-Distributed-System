import sys
import xmlrpc.client
import threading
import time

NUM_REQUESTS = int(sys.argv[1])
TEST_TEXT = "Eres un tontolaba_1 y un tontolaba_2"

def worker(server_uri, requests):
    try:
        server = xmlrpc.client.ServerProxy(server_uri)

        for _ in range(requests):
            server.censor_text(TEST_TEXT)
    except Exception as e:
        print(f"Error en worker (FilterClient): {e}")

# Registrar inicio
global_start = time.time()

# Obtener servidores
try:
    name_server = xmlrpc.client.ServerProxy("http://localhost:9000/RPC2")
    servers = name_server.get_servers()
    if not servers:
        raise Exception("No hay servidores registrados")
except Exception as e:
    print(f"Error al obtener servidores: {e}")
    sys.exit(1)

# Ejecutar threads
threads = []
requests_per_server = max(1, NUM_REQUESTS // len(servers))

for uri in servers:
    t = threading.Thread(
        target=worker,
        args=(uri, requests_per_server)
    )
    t.start()
    threads.append(t)

# Esperar finalización
for t in threads:
    t.join()

# Calcular métricas
total_time = time.time() - global_start

# Guardar resultados
with open("tiempos_clientes.log", "a") as f:
    f.write(
        f"FilterClient,{NUM_REQUESTS},{len(servers)},"
        f"{total_time:.4f}\n"
    )

print("FilterClient Acabado")
print(f"  Total: {total_time:.2f}s")