import Pyro4

@Pyro4.expose
class InsultSubscriber:
    def receive_insult(self, insult):
        print(f"\n¡INSULTO RECIBIDO!: {insult}")

def main():
    ns = Pyro4.locateNS()
    publisher = Pyro4.Proxy("PYRONAME:publisher.insultos")
    
    with Pyro4.Daemon() as daemon:
        subscriber = InsultSubscriber()
        subscriber_uri = daemon.register(subscriber)
        
        if publisher.subscribe(subscriber_uri):
            print(f"Suscriptor registrado con URI: {subscriber_uri}")
            print("Esperando insultos... (Ctrl+C para salir)")
            daemon.requestLoop()
        else:
            print("Error al registrar suscriptor")

if __name__ == "__main__":
    main()