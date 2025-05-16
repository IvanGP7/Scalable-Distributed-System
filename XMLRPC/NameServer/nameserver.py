from xmlrpc.server import SimpleXMLRPCServer
import threading

class NameServer:
    def __init__(self):
        self.servers = []
        self.lock = threading.Lock()

    def register_server(self, uri):
        with self.lock:
            if uri not in self.servers:
                self.servers.append(uri)
                print(f"Servidor registrado: {uri}")
                return True
        return False

    def get_servers(self):
        return self.servers

server = SimpleXMLRPCServer(('localhost', 9000))
server.register_instance(NameServer())
print("NameServer listo en puerto 9000")
server.serve_forever()