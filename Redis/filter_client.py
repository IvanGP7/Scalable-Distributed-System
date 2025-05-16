import redis
import threading
import time
import sys
from Functions_insult import InsultManager

TEST_TEXT = "Eres un bobo, zoquete y un TONTOLABA de mierda"

def worker(requests, r, results):
    manager = InsultManager(r)
    start = time.time()
    
    for _ in range(requests):
        manager.censor_text(TEST_TEXT)
    
    end = time.time()
    results.append(end - start)

def main():
    if len(sys.argv) != 3:
        print("Uso: python filter_client.py <num_peticiones> <num_threads>")
        return

    num_requests = int(sys.argv[1])
    num_threads = int(sys.argv[2])
    
    r = redis.Redis(host='localhost', port=6379, db=0)
    results = []
    requests_per_thread = num_requests // num_threads

    print(f"\nFilterClient: {num_requests} peticiones, {num_threads} threads")
    print(f"Texto de prueba: '{TEST_TEXT}'")
    
    start_time = time.time()
    threads = []
    
    for _ in range(num_threads):
        t = threading.Thread(
            target=worker,
            args=(requests_per_thread, r, results)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_time = time.time() - start_time
    
    with open("tiempos_clientes.log", "a") as f:
        f.write(f"FilterClient,{num_requests},{num_threads},{total_time:.4f}\n")
    
    print(f"Finalizado en {total_time:.2f} segundos")
    print(f"Resultados guardados en tiempos_clientes.log")

if __name__ == "__main__":
    main()