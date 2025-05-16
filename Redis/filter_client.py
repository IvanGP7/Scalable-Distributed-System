import redis
import threading
import time
import sys

TEST_TEXT = "Eres un bobo, tontolaba y un insulto_0_1"

def worker(requests):
    r = redis.Redis(host='localhost', port=6379, db=0)
    for _ in range(requests):
        insults = [i.decode('utf-8') for i in r.lrange("global_insults", 0, -1)]
        # Obtener la lista de insultos
        if insults:
            import re
            re.sub('|'.join(map(re.escape, insults)), 'CENSORED', TEST_TEXT)

if __name__ == "__main__":
    num_requests = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    start = time.time()
    threads = []

    requests_per_worker = max(1, num_requests // num_workers)

    for _ in range(num_workers):
        t = threading.Thread(target=worker, args=(requests_per_worker,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    total_time = time.time() - start

    with open("tiempos_clientes.log", "a") as f:
        f.write(f"FilterClient,{num_requests},{num_workers},{total_time:.4f}\n")

    print(f"FilterClient - {num_requests} censuras - {num_workers} workers")
    print(f"Tiempo: {total_time:.2f}s")