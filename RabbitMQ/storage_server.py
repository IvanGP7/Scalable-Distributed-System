import pika
import json
import time
from threading import Thread, Lock

class StorageServer:
    def __init__(self):
        self.insults = set(["BOBO", "TONTOLABA"])  # Usamos set para evitar duplicados
        self.lock = Lock()
        self.setup_rabbitmq()
        
    def setup_rabbitmq(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        
        # Exchange para sincronización
        self.channel.exchange_declare(exchange='insults_sync', exchange_type='fanout')
        
        # Cola para recibir actualizaciones
        self.channel.queue_declare(queue='storage_updates')
        self.channel.queue_bind(exchange='insults_sync', queue='storage_updates')
        
        # Cola para peticiones
        self.channel.queue_declare(queue='storage_requests')
        
    def handle_update(self, ch, method, properties, body):
        new_insults = json.loads(body).get('insults', [])
        with self.lock:
            updated = False
            for insult in new_insults:
                if insult not in self.insults:
                    self.insults.add(insult)
                    updated = True
                    print(f"[Storage] Nuevo insulto registrado: {insult}")
            
            if updated:
                self.broadcast_insults()
    
    def broadcast_insults(self):
        """Envía la lista completa a todos los workers"""
        with self.lock:
            insults_list = list(self.insults)
        
        self.channel.basic_publish(
            exchange='insults_sync',
            routing_key='',
            body=json.dumps({'insults': insults_list})
        )
        print("[Storage] Lista de insultos actualizada y enviada")
    
    def sync_loop(self):
        """Envía sincronizaciones periódicas"""
        while True:
            time.sleep(5)
            self.broadcast_insults()
    
    def start(self):
        # Consumir actualizaciones
        self.channel.basic_consume(
            queue='storage_updates',
            on_message_callback=self.handle_update,
            auto_ack=True
        )
        
        # Iniciar hilo de sincronización periódica
        sync_thread = Thread(target=self.sync_loop)
        sync_thread.daemon = True
        sync_thread.start()
        
        print("[Storage Server] Iniciado y listo")
        self.channel.start_consuming()

if __name__ == "__main__":
    server = StorageServer()
    server.start()