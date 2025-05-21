import pika
import re
import json
import threading

class InsultWorker:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.insults = set(["BOBO", "TONTOLABA"])
        self.lock = threading.Lock()
        self.setup_rabbitmq()

    def setup_rabbitmq(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        
        # Colas principales
        self.channel.queue_declare(queue='add_insults')
        self.channel.queue_declare(queue='filter_text')
        
        # Configuración para sincronización
        self.channel.exchange_declare(exchange='insults_sync', exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.sync_queue = result.method.queue
        self.channel.queue_bind(exchange='insults_sync', queue=self.sync_queue)
        
        # Configurar calidad de servicio
        self.channel.basic_qos(prefetch_count=1)

    def process_message(self, ch, method, props, body):
        try:
            if method.routing_key == 'add_insults':
                self._process_insult(body)
            elif method.routing_key == 'filter_text':
                self._process_filter(body, props)
            
            # Enviar confirmación
            if props.reply_to:
                ch.basic_publish(
                    exchange='',
                    routing_key=props.reply_to,
                    body='ACK'
                )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"[Worker {self.worker_id}] Error: {str(e)}")

    def _process_insult(self, body):
        insult = body.decode()
        with self.lock:
            if insult not in self.insults:
                self.insults.add(insult)
                print(f"[Worker {self.worker_id}] Nuevo insulto: {insult}")
                # Enviar a storage (implementación anterior)

    def _process_filter(self, body, props):
        text = body.decode()
        with self.lock:
            pattern = re.compile('|'.join(map(re.escape, self.insults)), re.IGNORECASE)
        
        censored = pattern.sub('CENSURADO', text)
        
        with threading.Lock():
            with open("insults.txt", "a") as f:
                f.write(f"{censored}\n")

    def start(self):
        # Configurar consumers
        self.channel.basic_consume(
            queue='add_insults',
            on_message_callback=self.process_message
        )
        
        self.channel.basic_consume(
            queue='filter_text',
            on_message_callback=self.process_message
        )
        
        self.channel.basic_consume(
            queue=self.sync_queue,
            on_message_callback=lambda ch, method, props, body: self._sync_insults(body)
        )
        
        print(f"[Worker {self.worker_id}] Iniciado")
        self.channel.start_consuming()

    def _sync_insults(self, body):
        data = json.loads(body)
        with self.lock:
            self.insults.update(data.get('insults', []))

if __name__ == "__main__":
    import sys
    worker_id = sys.argv[1] if len(sys.argv) > 1 else 1
    worker = InsultWorker(worker_id)
    worker.start()