import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='add_insults')

# Enviar N insultos de prueba
for i in range(1, 6):
    insult = f"INSULTO_{i}"
    channel.basic_publish(
        exchange='',
        routing_key='add_insults',
        body=insult
    )
    print(f"Enviado: {insult}")

connection.close()