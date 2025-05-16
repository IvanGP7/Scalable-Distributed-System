import pika
import time
from Functions_insult import InsultManager

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare exchange for pub/sub
channel.exchange_declare(exchange='insults_exchange', exchange_type='fanout')
insult_manager = InsultManager(channel)

print("Publisher listo. Enviando insultos cada 5 segundos...")

while True:
    time.sleep(5)
    insult = insult_manager.random_insult()
    print(f"Enviando insulto: {insult}")
    channel.basic_publish(
        exchange='insults_exchange',
        routing_key='',
        body=insult,
        properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
    )