import pika
import json
import re

class InsultWorker:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        
        # Declarar colas
        self.channel.queue_declare(queue='add_insults')
        self.channel.queue_declare(queue='filter_text')
        
        # Lista en memoria (persistiría en DB en producción)
        self.insults = ["BOBO", "TONTOLABA"]  # Valores iniciales

    def handle_add(self, ch, method, properties, body):
        insult = body.decode()
        if insult not in self.insults:
            self.insults.append(insult)
            print(f"Insulto añadido: {insult}")
        
    def handle_filter(self, ch, method, properties, body):
        text = body.decode()
        pattern = re.compile('|'.join(map(re.escape, self.insults)), re.IGNORECASE)
        censored = pattern.sub('CENSORED', text)
        
        with open("insults.txt", "a") as f:
            f.write(f"{censored}\n")
        
        print(f"Texto censurado guardado")

    def start(self):
        # Configurar consumers
        self.channel.basic_consume(
            queue='add_insults',
            on_message_callback=self.handle_add,
            auto_ack=True
        )
        
        self.channel.basic_consume(
            queue='filter_text',
            on_message_callback=self.handle_filter,
            auto_ack=True
        )
        
        print("Worker listo. Esperando mensajes...")
        self.channel.start_consuming()

if __name__ == "__main__":
    worker = InsultWorker()
    worker.start()