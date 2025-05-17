import random
import json
import pika
import re

class InsultManager:
    def __init__(self, channel):
        self.channel = channel
        self.queue_name = 'insults_queue'
        self.default_insults = ["BOBO", "ZOQUETE", "GILIPOLLAS", "INEPTO", "MONONEURONAL", "RETRASADO"]
        self._initialize_insults()

    def _initialize_insults(self):
        """Initialize insults queue with default values if empty"""
        if self.channel.queue_declare(queue=self.queue_name, durable=True).method.message_count == 0:
            for insult in self.default_insults:
                self._persist_insult(insult)

    def _persist_insult(self, insult):
        """Store insult in persistent queue"""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=insult,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def add_insult(self, insult):
        """Add new insult if not exists"""
        if insult not in self.insult_list():
            self._persist_insult(insult)
            print(f"{insult} añadido a la lista")
            return True
        print(f"{insult} ya existe en la lista")
        return False

    def random_insult(self):
        """Get random insult from queue"""
        insults = self.insult_list()
        if not insults:
            return "No hay insultos disponibles"
        return random.choice(insults)

    def insult_list(self):
        """Get all insults from queue"""
        insults = []
        method_frame, header_frame, body = self.channel.basic_get(queue=self.queue_name, auto_ack=False)
        
        while method_frame:
            insults.append(body.decode())
            self.channel.basic_ack(method_frame.delivery_tag)
            method_frame, header_frame, body = self.channel.basic_get(queue=self.queue_name, auto_ack=False)
        
        for insult in insults:
            self._persist_insult(insult)
            
        return insults

    def clear_insults(self):
        """Clear all insults from queue"""
        self.channel.queue_purge(queue=self.queue_name)
        self._initialize_insults()
        print("Lista de insultos borrada y reinicializada")
        return True

    def censor_text(self, text):
        """Censors insults in text replacing them with 'CENSORED'"""
        insults = self.insult_list()
        pattern = re.compile('|'.join(map(re.escape, insults)), re.IGNORECASE)
        censored_text = pattern.sub('CENSORED', text)
        return censored_text