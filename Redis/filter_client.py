import redis
import time
import sys
import json

TEST_TEXT = "Eres un bobo, zoquete y un TONTOLABA de mierda"

def main():
    if len(sys.argv) != 3:
        print("Uso: python filter_client.py <num_peticiones> <num_threads>")
        return

    num_requests = int(sys.argv[1])
    num_threads = int(sys.argv[2])
    client_name = "filter"

    r = redis.Redis(host='localhost', port=6379, db=0)

    # Inicializar contador en Redis
    r.set(f"{client_name}_done", 0)

    print(f"\nFilterClient: {num_requests} peticiones delegadas a filter_queue")
    print(f"Texto de prueba: '{TEST_TEXT}'")

    start_time = time.time()

    for _ in range(num_requests):
        task = json.dumps({"text": TEST_TEXT})
        r.rpush("filter_queue", task)

    # Esperar hasta que todas las tareas sean procesadas
    while int(r.get(f"{client_name}_done")) < num_requests:
        time.sleep(0.1)

    total_time = time.time() - start_time

    with open("tiempos_clientes.log", "a") as f:
        f.write(f"FilterClient,{num_threads},{num_requests},{total_time:.4f}\n")

    print(f"Finalizado en {total_time:.2f} segundos")

if __name__ == "__main__":
    main()
