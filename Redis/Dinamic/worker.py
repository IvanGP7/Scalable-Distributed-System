import redis
import threading
import time
from Functions_insult import InsultManager

class Worker(threading.Thread):
    def __init__(self, redis_conn, stop_event):
        super().__init__(daemon=True)
        self.redis_conn = redis_conn
        self.stop_event = stop_event
        self.manager = InsultManager(redis_conn)

    def run(self):
        while not self.stop_event.is_set():
            task = self.redis_conn.brpop('task_queue', timeout=1)
            if task:
                text = task[1].decode('utf-8')
                self.manager.censor_text(text)

def scaler(redis_conn, workers, stop_event, min_workers=1, max_workers=10, check_interval=2):
    while not stop_event.is_set():
        current_length = redis_conn.llen('task_queue')
        current_workers = len(workers)
        
        # Lógica de escalado
        if current_length > current_workers * 2 and current_workers < max_workers:
            worker_stop = threading.Event()
            worker = Worker(redis_conn, worker_stop)
            workers.append((worker, worker_stop))
            worker.start()
            with open("worker.log", "a") as f:
                f.write(f"Escalando a {len(workers)} workers\n")
            print(f"Escalando a {len(workers)} workers")
        elif current_length == 0 and current_workers > min_workers:
            worker, worker_stop = workers.pop()
            worker_stop.set()
            worker.join()
            with open("worker.log", "a") as f:
                f.write(f"Reduciendo a {len(workers)} workers\n")
            print(f"Reduciendo a {len(workers)} workers")
        
        time.sleep(check_interval)

def main():
    r = redis.Redis(host='localhost', port=6379, db=0)
    stop_event = threading.Event()
    workers = []
    
    # Workers iniciales
    for _ in range(1):
        worker_stop = threading.Event()
        worker = Worker(r, worker_stop)
        workers.append((worker, worker_stop))
        worker.start()
    
    # Hilo escalador
    scaler_thread = threading.Thread(
        target=scaler, 
        args=(r, workers, stop_event),
        daemon=True
    )
    scaler_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        for worker, worker_stop in workers:
            worker_stop.set()
        with open("worker.log", "a") as f:
            f.write("\nDeteniendo todos los workers...\n")
        print("\nDeteniendo todos los workers...")
        for worker, _ in workers:
            worker.join()

if __name__ == "__main__":
    main()