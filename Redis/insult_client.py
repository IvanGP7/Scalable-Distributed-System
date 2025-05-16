import redis
import threading
import time
import sys

def worker(worker_id, requests):
r = redis.Redis(host='localhost', port=6379, db=0)
for i in range(requests):
    r.rpush("global_insults", f"insult_{worker_id}_{i}")

if __name__ == "__main__":
num_requests = int(sys.argv[1]) if len(sys.argv) > 1 else 10
num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 3

start = time.time()
threads = []

requests_per_worker = max(1, num_requests // num_workers)

for i in range(num_workers):
    t = threading.Thread(target=worker, args=(i, requests_per_worker))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

total_time = time.time() - start

with open("tiempos_clientes.log", "a") as f:
    f.write(f"InsultClient,{num_requests},{num_workers},{total_time:.4f}\n")

print(f"InsultClient - {num_requests} adds - {num_workers} workers")
print(f"Tiempo: {total_time:.2f}s")