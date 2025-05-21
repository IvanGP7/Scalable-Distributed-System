import pika
import time
import sys
import threading
import random

TEXTS = [
    "Eres un bobo y un TONTOLABA",
    "Los bobos no saben programar",
    "Deja de ser tan INSULTO_3"
]

class FilterClient:
    def __init__(self, num_requests, worker_id):
        self.num_requests = num_requests
        self.worker_id = worker_id
        self.processed = 0
        self.lock = threading.Lock()
        self.start_time = None

    def on_response(self, ch, method, properties, body):
        with self.lock:
            self.processed += 1
            if self.processed >= self.num_requests:
                ch.stop_consuming()


    def _save_time(self, elapsed):
        with open("tiempos_clientes.log", "a") as f:
            f.write(f"FilterClient,{self.num_requests},{self.worker_id},{elapsed:.4f}\n")

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        
        # Cola de respuesta
        result = channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        
        channel.basic_consume(
            queue=callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        
        
        # Enviar mensajes
        for _ in range(self.num_requests):
            text = random.choice(TEXTS)
            channel.basic_publish(
                exchange='',
                routing_key='filter_text',
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                ),
                body=text
            )

        # Esperar confirmaciones
        channel.start_consuming()
        connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python filter_client.py <num_requests> <worker_id>")
        sys.exit(1)
    start_time = time.perf_counter()
    client = FilterClient(int(sys.argv[1]), int(sys.argv[2]))
    client.run()
    elapsed = time.perf_counter() - start_time
    client._save_time(elapsed)