from xmlrpc.server import SimpleXMLRPCServer
import threading

class Storage:
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
        with self.lock:
            return self.insults.copy()  # Devolver copia para thread safety

    def get_random(self):
        with self.lock:
            if not self.insults:
                return None
            import random
            return random.choice(self.insults)

server = SimpleXMLRPCServer(('localhost', 9100))
server.register_instance(Storage())
print("StorageServer listo en puerto 9100")
server.serve_forever()