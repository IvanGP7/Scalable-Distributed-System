import redis
import time
from Functions_insult import InsultManager

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
insult_manager = InsultManager(r)

print("Publisher listo. Enviando insultos cada 5 segundos...")

while True:
    time.sleep(5)
    insult = insult_manager.random_insult()
    print(f"Enviando insulto: {insult}")
    r.publish('insultos', insult)