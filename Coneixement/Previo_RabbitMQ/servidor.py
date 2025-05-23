import pika
from Functions_insult import InsultManager

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue for insults persistence
channel.queue_declare(queue='insults_queue', durable=True)
insult_manager = InsultManager(channel)

print("Servidor de insultos listo. Usando RabbitMQ como backend.")
print("Lista inicial:", insult_manager.insult_list())

# Keep server running
connection.close()