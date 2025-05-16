import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import threading
import time
import re

PORT = int(sys.argv[1])
STORAGE_URI = "http://localhost:9100/RPC2"
NAME_URI = "http://localhost:9000/RPC2"
SYNC_INTERVAL = 4  # Sincronizar cada 4 segundos

class InsultServer:
    def __init__(self):
        self.storage = xmlrpc.client.ServerProxy(STORAGE_URI)
        self.local_insults = []
        self.lock = threading.Lock()
        self.sync_insults()  # Sincronización inicial
        threading.Thread(target=self.sync_loop, daemon=True).start()

    def sync_loop(self):
        while True:
            time.sleep(SYNC_INTERVAL)
            self.sync_insults()

    def sync_insults(self):
        try:
            new_insults = self.storage.get_insults()
            with self.lock:
                self.local_insults = new_insults
        except Exception as e:
            print(f"Error sincronizando insultos: {e}")

    def add_insult(self, insult):
        try:
            # Primero añadir al Storage
            if self.storage.add_insult(insult):
                with self.lock:
                    if insult not in self.local_insults:
                        self.local_insults.append(insult)
                return True
            return False
        except Exception as e:
            print(f"Error añadiendo insulto: {e}")
            return False

    def get_insult(self):
        with self.lock:
            if not self.local_insults:
                return None
            import random
            return random.choice(self.local_insults)

    def censor_text(self, text):
        with self.lock:
            if not self.local_insults:
                return text
                

            pattern = re.compile('|'.join(map(re.escape, self.local_insults)), re.IGNORECASE)
            return pattern.sub('CENSORED', text)

server = SimpleXMLRPCServer(('localhost', PORT))
server.register_instance(InsultServer())

# Registrar en NameServer
try:
    name_server = xmlrpc.client.ServerProxy(NAME_URI)
    name_server.register_server(f"http://localhost:{PORT}/RPC2")
    print(f"Servidor listo en puerto {PORT}")
    server.serve_forever()
except Exception as e:
    print(f"Error registrando servidor: {e}")
    sys.exit(1)