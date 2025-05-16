import redis
from Functions_insult import InsultManager

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)
insult_manager = InsultManager(r)

def test_system():
    print("\n=== TEST CLIENTE ===")
    print("Lista actual:", insult_manager.insult_list())
    
    # Test añadir insulto
    new_insult = "TONTOLABA"
    print(f"\nAñadiendo '{new_insult}'...")
    if insult_manager.add_insult(new_insult):
        print("¡Añadido con éxito!")
    else:
        print("Ya existía")
    
    # Test de censura
    test_text = "Eres un bobo y un zoquete, además de medio TontoLaba y un inepTo"
    print("\n=== TEST DE CENSURA ===")
    print("Texto original:", test_text)
    print("Texto censurado:", insult_manager.censor_text(test_text))
    

if __name__ == "__main__":
    test_system()