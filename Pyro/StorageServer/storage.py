import Pyro4
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class StorageServer:
    def __init__(self):
        self.insults = []
        self.lock = threading.Lock()

    def add_insult(self, insult):
        with self.lock:
            if insult not in self.insults:
                self.insults.append(insult)
                return True
        return False

    def get_insults(self):
        return self.insults.copy()

def start_storage():
    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS()
    uri = daemon.register(StorageServer)
    ns.register("storage.node", uri)
    print("StorageServer listo")
    daemon.requestLoop()

if __name__ == "__main__":
    start_storage()