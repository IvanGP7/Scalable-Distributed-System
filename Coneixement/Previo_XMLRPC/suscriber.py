from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

class Subscriber:
    def receive_insult(self, insult):
        print(f"\n¡INSULTO RECIBIDO!: {insult}")
        return True

def start_subscriber(port):
    subscriber = Subscriber()
    server = SimpleXMLRPCServer(('localhost', port))
    server.register_instance(subscriber)
    
    # Registrarse en el publisher
    publisher = xmlrpc.client.ServerProxy("http://localhost:8001/RPC2")
    if publisher.subscribe(f"http://localhost:{port}/RPC2"):
        print(f"Suscriptor escuchando en http://localhost:{port}")
        print("Esperando insultos... (Ctrl+C para salir)")
        server.serve_forever()
    else:
        print("Error al registrar suscriptor")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        start_subscriber(int(sys.argv[1]))
    else:
        print("Uso: python suscriber.py <puerto>")