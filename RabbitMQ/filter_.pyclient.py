import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='filter_text')

texts = [
    "Eres un bobo y un TONTOLABA",
    "Los bobos no saben programar",
    "Deja de ser tan INSULTO_3"
]

for text in texts:
    channel.basic_publish(
        exchange='',
        routing_key='filter_text',
        body=text
    )
    print(f"Enviado a censurar: {text}")
    time.sleep(0.5)

connection.close()