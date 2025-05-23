import redis
from Functions_insult import InsultManager

r = redis.Redis(host='localhost', port=6379, db=0)
insult_manager = InsultManager(r)

print("Servidor de insultos listo. Usando Redis como backend.")
print("Lista inicial:", insult_manager.insult_list())

# Mantener el servidor corriendo
while True:
    pass