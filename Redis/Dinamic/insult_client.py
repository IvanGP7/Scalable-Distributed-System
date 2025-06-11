import redis
import threading
import time
import sys

def submit_insults(num_requests, redis_conn):
    for i in range(num_requests):
        insult = f"insult_{i}"
        redis_conn.lpush('task_queue', insult)

def main():
    if len(sys.argv) != 3:
        print("Uso: python insult_client.py <num_peticiones> <num_threads>")
        return

    num_requests = int(sys.argv[1])
    num_threads = int(sys.argv[2])

    r = redis.Redis(host='localhost', port=6379, db=0)
    r.delete('task_queue')  # Limpiar cola previa si existe

    print(f"\nEnviando {num_requests} insultos con {num_threads} threads")
    start_time = time.time()

    requests_per_thread = num_requests // num_threads
    threads = []

    for _ in range(num_threads):
        t = threading.Thread(target=submit_insults, args=(requests_per_thread, r))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Esperar hasta que todos los insultos sean procesados por los workers
    while r.llen('task_queue') > 0:
        time.sleep(0.1)

    total_time = time.time() - start_time

    with open("tiempos_clientes.log", "a") as f:
        f.write(f"InsultClient,{num_requests},{num_threads},{total_time:.4f}\n")

    print(f"Tiempo total: {total_time:.2f}s")

if __name__ == "__main__":
    main()
