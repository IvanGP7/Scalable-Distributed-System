import random
import re

lista_insultos = ["BOBO", "ZOQUETE", "GILIPOLLAS", "INEPTO", "MONONEURONAL", "RETRASADO"]

def add_insult(insulto):
    if insulto.upper() not in [i.upper() for i in lista_insultos]:
        lista_insultos.append(insulto.upper())
        print(f"{insulto} añadido a la lista")
        return True
    print(f"{insulto} ya existe en la lista")
    return False

def random_insult():
    return random.choice(lista_insultos) if lista_insultos else "No hay insultos disponibles"

def insult_list():
    return lista_insultos

def clear_insults():
    global lista_insultos
    lista_insultos.clear()
    print("Lista de insultos borrada")
    return True

def censor_text(text):
    """Censura insultos en el texto reemplazándolos por 'CENSORED'"""
    if not lista_insultos:
        return text
        
    pattern = re.compile('|'.join(map(re.escape, lista_insultos)), re.IGNORECASE)
    return pattern.sub('CENSORED', text)