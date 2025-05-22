import random
import re

class InsultManager:
    def __init__(self, redis_conn):
        self.r = redis_conn
        self.key = "lista_insultos"
        # Inicializar con valores por defecto si no existen
        if not self.r.exists(self.key):
            default_insults = ["BOBO", "ZOQUETE", "GILIPOLLAS", "INEPTO", "MONONEURONAL", "RETRASADO"]
            self.r.rpush(self.key, *default_insults)

    def add_insult(self, insulto):
        """Añade un nuevo insulto si no existe"""
        if not self.r.lrem(self.key, 0, insulto):
            self.r.rpush(self.key, insulto)
            print(f"{insulto} añadido a la lista")
            return True
        print(f"{insulto} ya existe en la lista")
        return False

    def random_insult(self):
        """Devuelve un insulto aleatorio"""
        list_length = self.r.llen(self.key)
        if list_length == 0:
            return "No hay insultos disponibles"
        random_index = random.randint(0, list_length - 1)
        return self.r.lindex(self.key, random_index).decode('utf-8')

    def insult_list(self):
        """Devuelve la lista completa de insultos"""
        return [insult.decode('utf-8') for insult in self.r.lrange(self.key, 0, -1)]

    def clear_insults(self):
        """Limpia la lista de insultos"""
        self.r.delete(self.key)
        print("Lista de insultos borrada")
        return True

    def censor_text(self, text):
        """Censura insultos en un texto reemplazándolos por 'CENSORED'"""
        insults = self.insult_list()
        if not insults:
            return text
            
        # Creamos un patrón regex que ignora mayúsculas/minúsculas
        pattern = re.compile('|'.join(map(re.escape, insults)), re.IGNORECASE)
        
        # Reemplazamos todas las ocurrencias
        censored_text = pattern.sub('CENSORED', text)
        return censored_text