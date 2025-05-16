import Pyro4
import threading

@Pyro4.expose
class WorkerNode:
    def __init__(self):
        self.insults = []
        self.lock = threading.Lock()
        self.storage = Pyro4.Proxy("PYRONAME:storage.node")

    def update_insults(self, new_insults):
        with self.lock:
            self.insults = new_insults.copy()

    def add_insult(self, insult):
        success = self.storage.add_insult(insult)
        if success:
            with self.lock:
                if insult not in self.insults:
                    self.insults.append(insult)
        return success

    def censor_text(self, text):
        with self.lock:
            if not self.insults:
                return text
            import re
            pattern = re.compile('|'.join(map(re.escape, self.insults)), re.IGNORECASE)
            return pattern.sub('CENSORED', text)

def start_worker(worker_id):
    daemon = Pyro4.Daemon(host="localhost")
    worker = WorkerNode()
    uri = daemon.register(worker)
    
    # Registrar en NameServer
    nameserver = Pyro4.Proxy("PYRONAME:nameserver.node")
    nameserver.register_worker(uri)
    
    print(f"Worker {worker_id} listo")
    daemon.requestLoop()

if __name__ == "__main__":
    import sys
    worker_id = sys.argv[1] if len(sys.argv) > 1 else "1"
    start_worker(worker_id)