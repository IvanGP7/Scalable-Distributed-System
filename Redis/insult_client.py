import redis
import time
import sys
import json

def main():
    if len(sys.argv) != 3:
        print("Uso: python insult_client.py <num_peticiones> <num_threads>")
        return

    num_requests = int(sys.argv[1])
    num_threads = int(sys.argv[2])
    client_name = "insult"

    r = redis.Redis(host='localhost', port=6379, db=0)

    # Inicializar contador en Redis
    r.set(f"{client_name}_done", 0)

    print(f"\nInsultClient: {num_requests} peticiones delegadas a insult_queue")

    start_time = time.time()

    for i in range(num_requests):
        insult = f"insult_{i}"
        task = json.dumps({"insult": insult})
        r.rpush("insult_queue", task)

    # Esperar hasta que todas las tareas sean procesadas
    while int(r.get(f"{client_name}_done")) < num_requests:
        time.sleep(0.1)

    total_time = time.time() - start_time

    with open("tiempos_clientes.log", "a") as f:
        f.write(f"InsultClient,{num_threads},{num_requests},{total_time:.4f}\n")

    print(f"Finalizado en {total_time:.2f} segundos")

if __name__ == "__main__":
    main()
