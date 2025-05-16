import redis

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('insultos')

print("Suscriptor listo. Esperando insultos...")

for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"\n¡INSULTO RECIBIDO!: {message['data'].decode('utf-8')}")