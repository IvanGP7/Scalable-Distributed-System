import pika

def callback(ch, method, properties, body):
    print(f"\n¡INSULTO RECIBIDO!: {body.decode()}")

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare exchange and queue
channel.exchange_declare(exchange='insults_exchange', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='insults_exchange', queue=queue_name)

print("Suscriptor listo. Esperando insultos...")
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True)

channel.start_consuming()