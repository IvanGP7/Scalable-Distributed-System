import random
import re
import Pyro4

@Pyro4.expose
class InsultManager:
    def __init__(self):
        self.lista_insultos = ["BOBO", "ZOQUETE", "GILIPOLLAS", "INEPTO", "MONONEURONAL", "RETRASADO"]

    @Pyro4.expose
    def add_insult(self, insulto):
        if insulto.upper() not in [i.upper() for i in self.lista_insultos]:
            self.lista_insultos.append(insulto.upper())
            print(f"{insulto} añadido a la lista")
            return True
        print(f"{insulto} ya existe en la lista")
        return False

    @Pyro4.expose
    def random_insult(self):
        return random.choice(self.lista_insultos) if self.lista_insultos else "No hay insultos disponibles"

    @Pyro4.expose
    def insult_list(self):
        return self.lista_insultos

    @Pyro4.expose
    def clear_insults(self):
        self.lista_insultos.clear()
        print("Lista de insultos borrada")
        return True

    @Pyro4.expose
    def censor_text(self, text):
        """Censura insultos en el texto reemplazándolos por 'CENSORED'"""
        if not self.lista_insultos:
            return text
            
        pattern = re.compile('|'.join(map(re.escape, self.lista_insultos)), re.IGNORECASE)
        return pattern.sub('CENSORED', text)