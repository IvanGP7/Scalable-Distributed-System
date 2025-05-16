import xmlrpc.client
import time
import threading

subscribers = []
subscribers_lock = threading.Lock()

def notify_subscribers(insult):
    with subscribers_lock:
        for sub in subscribers[:]:
            try:
                sub.receive_insult(insult)
            except:
                print(f"Error notificando a suscriptor {sub}")
                subscribers.remove(sub)

def start_publisher():
    with xmlrpc.client.ServerProxy("http://localhost:8000/RPC2") as server:
        while True:
            time.sleep(5)
            insult = server.random_insult()
            print(f"Notificando insulto: {insult}")
            notify_subscribers(insult)

def subscribe(callback_url):
    with subscribers_lock:
        if callback_url not in subscribers:
            subscribers.append(xmlrpc.client.ServerProxy(callback_url))
            print("Nuevo suscriptor registrado:", callback_url)
            return True
    return False

# Configurar servidor para suscriptores
from xmlrpc.server import SimpleXMLRPCServer
publisher_server = SimpleXMLRPCServer(('localhost', 8001))
publisher_server.register_function(subscribe)
publisher_server.register_introspection_functions()

print("Publisher listo en http://localhost:8001")
threading.Thread(target=start_publisher, daemon=True).start()
publisher_server.serve_forever()