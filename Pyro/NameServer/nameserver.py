import Pyro4
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class NameServer:
    def __init__(self):
        self.workers = []
        self.lock = threading.Lock()

    def register_worker(self, worker_uri):
        with self.lock:
            if worker_uri not in self.workers:
                self.workers.append(worker_uri)
                print(f"Worker registrado: {worker_uri}")
                return True
        return False

    def get_workers(self):
        return self.workers

def start_nameserver():
    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS()
    uri = daemon.register(NameServer)
    ns.register("nameserver.node", uri)
    print("NameServer listo")
    daemon.requestLoop()

if __name__ == "__main__":
    start_nameserver()