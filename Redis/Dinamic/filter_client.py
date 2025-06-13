import redis
import time
import sys
import json
import threading

TEST_TEXT = "Eres un bobo, zoquete y un TONTOLABA de mierda"

def send_tasks(count, redis_conn, client_name):
    for _ in range(count):
        task = json.dumps({"text": TEST_TEXT})
        redis_conn.rpush("filter_queue", task)

def main():
    if len(sys.argv) != 3:
        print("Uso: python filter_client.py <num_peticiones> <num_threads>")
        return

    num_requests = int(sys.argv[1])
    num_threads = int(sys.argv[2])
    client_name = "filter"

    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(f"{client_name}_done", 0)

    print(f"\nFilterClient: {num_requests} peticiones delegadas a filter_queue")

    start_time = time.time()

    # Dividir trabajo entre threads
    tasks_per_thread = num_requests // num_threads
    remainder = num_requests % num_threads
    threads = []

    for i in range(num_threads):
        count = tasks_per_thread + (1 if i < remainder else 0)
        t = threading.Thread(target=send_tasks, args=(count, r, client_name))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Calcular tasa de llegada y guardarla en Redis
    duration = time.time() - start_time
    lambda_est = num_requests / duration if duration > 0 else 0
    r.set("lambda_estimate", lambda_est)

    # Esperar hasta que todas las tareas sean procesadas
    while int(r.get(f"{client_name}_done") or 0) < num_requests:
        time.sleep(0.1)

    total_time = time.time() - start_time

    with open("tiempos_clientes.log", "a") as f:
        f.write(f"FilterClient,{num_threads},{num_requests},{total_time:.4f}\n")

    print(f"Finalizado en {total_time:.2f} segundos")

if __name__ == "__main__":
    main()
