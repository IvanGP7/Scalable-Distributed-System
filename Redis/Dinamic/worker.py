import redis
import threading
import json
import time
import math
from Functions_insult import InsultManager
from redis.exceptions import ConnectionError
from collections import deque

# Historial de llegada de tareas para estimar λ
arrival_times = deque(maxlen=100)

class Worker(threading.Thread):
    def __init__(self, redis_conn, stop_event):
        super().__init__(daemon=True)
        self.redis_conn = redis_conn
        self.stop_event = stop_event
        self.manager = InsultManager(redis_conn)

    def run(self):
        while not self.stop_event.is_set():
            try:
                task = self.redis_conn.brpop(['insult_queue', 'filter_queue'], timeout=1)
                if task:
                    queue_name, content = task
                    queue_name = queue_name.decode()
                    content_str = content.decode('utf-8')

                    # Intentar decodificar JSON (en caso de que venga de filter_client)
                    try:
                        data = json.loads(content_str)
                        text = data.get("text", "")
                    except json.JSONDecodeError:
                        text = content_str

                    self.manager.censor_text(text)

                    # Actualizar el contador adecuado
                    if queue_name == "insult_queue":
                        self.redis_conn.incr("insult_done")
                    elif queue_name == "filter_queue":
                        self.redis_conn.incr("filter_done")
            except ConnectionError:
                print("[WARN] Redis desconectado. Worker deteniéndose.")
                break

def estimate_lambda():
    if len(arrival_times) < 2:
        return 0
    duration = arrival_times[-1] - arrival_times[0]
    if duration == 0:
        return 0
    return len(arrival_times) / duration

def record_arrival():
    arrival_times.append(time.time())

def scaler(redis_conn, workers, stop_event, min_workers=1, max_workers=15, check_interval=0.5):
    T_r = 1.0  # objetivo de respuesta
    T = 0.25   # tiempo medio de procesamiento
    C = 1 / T

    while not stop_event.is_set():
        try:
            B = redis_conn.llen('insult_queue') + redis_conn.llen('filter_queue')
            lambda_est = estimate_lambda()
            if lambda_est < 0.01:
                lambda_est = 10
        except ConnectionError:
            print("[WARN] Redis desconectado. Escalador deteniéndose.")
            break

        # Escalado con mayor resistencia a partir de B > 3000
        if B < 100:
            N = 1
        elif B >= 30000:
            N = max_workers
        else:
            N = int((B - 100) / (30000 - 100) * (max_workers - 1)) + 1

        N = max(min(N, max_workers), min_workers)
        current_workers = len(workers)

        print(f"[STATE] B={B}, lambda={lambda_est:.2f}, N={N}, workers={current_workers}", flush=True)

        if N > current_workers:
            for _ in range(N - current_workers):
                worker_stop = threading.Event()
                worker = Worker(redis_conn, worker_stop)
                workers.append((worker, worker_stop))
                worker.start()
            print(f"[INFO] Escalando a {len(workers)} workers")
            with open("worker.log", "a") as f:
                f.write(f"Escalando a {len(workers)} workers\n")

        elif N < current_workers:
            for _ in range(current_workers - N):
                worker, worker_stop = workers.pop()
                worker_stop.set()
                worker.join()
            print(f"[INFO] Reduciendo a {len(workers)} workers")
            with open("worker.log", "a") as f:
                f.write(f"Reduciendo a {len(workers)} workers\n")

        time.sleep(check_interval)

def main():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        stop_event = threading.Event()
        workers = []

        # Monitor de eventos de llegada (si usas una cola común tipo 'task_queue')
        pubsub = r.pubsub()
        pubsub.subscribe("__keyspace@0__:filter_queue")
        pubsub.subscribe("__keyspace@0__:insult_queue")

        def track():
            try:
                for msg in pubsub.listen():
                    if msg['type'] == 'message' and msg['data'] == b'lpush':
                        record_arrival()
            except ConnectionError:
                print("[WARN] Redis cerrado. Finalizando escucha de eventos.")

        monitor_thread = threading.Thread(target=track, daemon=True)
        monitor_thread.start()

        # Primer worker
        worker_stop = threading.Event()
        worker = Worker(r, worker_stop)
        workers.append((worker, worker_stop))
        worker.start()

        # Escalador dinámico
        scaler_thread = threading.Thread(
            target=scaler,
            args=(r, workers, stop_event),
            daemon=True
        )
        scaler_thread.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[EXIT] Interrupción recibida. Cerrando workers...")
        stop_event.set()
        for _, stop_evt in workers:
            stop_evt.set()
        for worker, _ in workers:
            worker.join()
        print("[DONE] Todos los workers detenidos.")
        with open("worker.log", "a") as f:
            f.write("\nDeteniendo todos los workers...\n")

if __name__ == "__main__":
    main()
