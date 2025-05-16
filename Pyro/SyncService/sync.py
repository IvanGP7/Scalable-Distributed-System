import Pyro4
import time
import threading

@Pyro4.expose
class SyncService:
    def __init__(self):
        self.storage = Pyro4.Proxy("PYRONAME:storage.node")
        self.interval = 5  # segundos

    def start_sync(self):
        while True:
            time.sleep(self.interval)
            self._sync_all()

    def _sync_all(self):
        insults = self.storage.get_insults()
        nameserver = Pyro4.Proxy("PYRONAME:nameserver.node")
        for worker_uri in nameserver.get_workers():
            try:
                worker = Pyro4.Proxy(worker_uri)
                worker.update_insults(insults)
            except:
                continue

def start_sync():
    daemon = Pyro4.Daemon(host="localhost")
    sync = SyncService()
    threading.Thread(target=sync.start_sync, daemon=True).start()
    ns = Pyro4.locateNS()
    uri = daemon.register(sync)
    ns.register("sync.node", uri)
    print("SyncService listo")
    daemon.requestLoop()

if __name__ == "__main__":
    start_sync()