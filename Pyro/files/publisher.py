import Pyro4
import threading
import time

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultPublisher:
    def __init__(self):
        self.subscribers = []
        self.lock = threading.Lock()

    def subscribe(self, subscriber_uri):
        with self.lock:
            subscriber = Pyro4.Proxy(subscriber_uri)
            if subscriber not in self.subscribers:
                self.subscribers.append(subscriber)
                print(f"Suscriptor {subscriber_uri} registrado")
                return True
        return False

    def unsubscribe(self, subscriber_uri):
        with self.lock:
            self.subscribers = [s for s in self.subscribers if str(s._pyroUri) != subscriber_uri]
            print(f"Suscriptor {subscriber_uri} eliminado")

    def notify_subscribers(self, insult):
        with self.lock:
            for sub in self.subscribers[:]:
                try:
                    sub.receive_insult(insult)
                except Pyro4.errors.CommunicationError:
                    print(f"Suscriptor {sub._pyroUri} desconectado")
                    self.subscribers.remove(sub)

def start_publisher():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    publisher = InsultPublisher()
    uri = daemon.register(publisher)
    ns.register("publisher.insultos", uri)
    
    print("Publisher listo. URI:", uri)
    
    # Hilo para notificaciones periódicas
    def notification_loop():
        server = Pyro4.Proxy("PYRONAME:servidor.insultos")
        while True:
            time.sleep(5)
            insult = server.random_insult()
            print(f"\nNotificando insulto: {insult}")
            publisher.notify_subscribers(insult)
    
    threading.Thread(target=notification_loop, daemon=True).start()
    daemon.requestLoop()

if __name__ == "__main__":
    start_publisher()