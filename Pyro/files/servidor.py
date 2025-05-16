import Pyro4
from Functions_insult import InsultManager

# python -m Pyro4.naming --host localhost --port 9090

daemon = Pyro4.Daemon(host="localhost")
ns = Pyro4.locateNS()
uri = daemon.register(InsultManager)
ns.register("servidor.insultos", uri)

print("Servidor listo. URI:", uri)
print("Insultos iniciales:", InsultManager().insult_list())
daemon.requestLoop()